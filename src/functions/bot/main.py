import functions_framework
import os
import json
from services.line_service import LineService
from services.llama_service import LlamaService
from services.storage_service import StorageService

@functions_framework.http
def run(request):
    # ライン署名情報を取得
    signature = request.headers.get('x-line-signature')
    body = request.get_data(as_text=True)

    # ライン署名の検証
    line_service = LineService(os.getenv('LINE_CHANNEL_SECRET'), os.getenv('LINE_ACCESS_TOKEN'))
    if not line_service.validate_signature(body, signature):
        print('署名検証に失敗しました。')
        return json.dumps({'message': 'Unauthorized'}), 401

    # ラインイベント、ユーザーのメッセージを取得
    line_event = json.loads(body)['events'][0]
    user_message = line_event['message']['text']

    # 生成AIに問い合わせ
    ai_response = ""
    try:
        # Google Cloud Storageからindexを取得
        storage_service = StorageService()
        bucket_name = os.getenv('BUCKET_NAME')
        file_name = os.getenv('QA_EMBEDDINGS_FILE_NAME')
        embeddings = storage_service.read_json_from_file(bucket_name, "qa", file_name)
        
        # 質問検索
        llamaService = LlamaService()
        llamaService.add_embeddings(embeddings)
        ai_response = llamaService.find_best_answer(user_message)
    except Exception as e:
        print('Open Ai Api エラー')
        print(f'Error occurred: {e}')
        return json.dumps(e), 500

    # 問い合わせ情報をラインに返信
    try:
        line_service.send_reply_to_line(line_event['replyToken'], ai_response)
        return json.dumps(ai_response), 200
    except Exception as e:
        print('Line Api エラー')
        print(f'Error occurred: {e}')
        return json.dumps(e), 500
