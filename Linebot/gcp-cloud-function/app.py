import os
import json
from services.line_service import LineService
from services.cloud.aws.storage_service import StorageService
from services.llama_service import LlamaService

def handler(event, context):
    # ライン署名情報を取得
    signature = event['headers'].get('x-line-signature')
    body = event['body']

    # ライン署名の検証
    line_service = LineService(os.getenv('LINE_CHANNEL_SECRET'), os.getenv('LINE_ACCESS_TOKEN'))
    if not line_service.validate_signature(body, signature):
        print('署名検証に失敗しました。')
        return {
            'statusCode': 401,
            'body': json.dumps({'message': 'Unauthorized'})
        }

    # ラインイベント、ユーザーのメッセージを取得
    line_event = json.loads(body)['events'][0]
    user_message = line_event['message']['text']

    # 生成AIに問い合わせ
    ai_response = ""
    try:
        # Google Cloud Storageからindexを取得
        aws_access_key_id = os.getenv('ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('SECRET_ACCESS_KEY')
        storage_service = StorageService(
            aws_access_key_id,
            aws_secret_access_key)
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
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }

    # 問い合わせ情報をラインに返信
    try:
        line_service.send_reply_to_line(line_event['replyToken'], ai_response)
        return {
            'statusCode': 200,
            'body': json.dumps(ai_response)
        }
    except Exception as e:
        print('Line Api エラー')
        print(f'Error occurred: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }