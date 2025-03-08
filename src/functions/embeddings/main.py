import functions_framework
import json
import os
from services.openai_service import OpenAiService
from services.storage_service import StorageService

@functions_framework.http
def run(request):
    # リクエストボディからQAデータを取得
    try:
        body = json.loads(request.get_data(as_text=True))
        if not body or 'qaData' not in body:
            return {
                'statusCode': 400,
                'body': json.dumps('リクエストボディにQAデータが含まれていません。')
            }
        qa_data = body['qaData']
    except (KeyError, json.JSONDecodeError):
        return {
            'statusCode': 400,
            'body': json.dumps('無効なリクエストボディです。')
        }

    # INDEX化
    try:
        openai_service = OpenAiService()
        embeddings = openai_service.generate_embeddings(qa_data)
    except Exception as error:
        print('Open Ai Api エラー')
        print('Error occurred', error)
        return {
            'statusCode': 500,
            'body': json.dumps('Error occurred')
        }

    # ベクトル化ファイルを保存
    storage_service = StorageService()
    index_file_name = os.environ.get('QA_EMBEDDINGS_FILE_NAME')
    qa_index_bucket_name = os.environ.get('BUCKET_NAME')
    try:
        storage_service.write_json_to_file(qa_index_bucket_name, 'qa', index_file_name, embeddings)
        return {
            'statusCode': 200,
            'body': json.dumps('ベクトル化に成功しました。')
        }
    except Exception as error:
        print('S3 Write エラー')
        print('Error occurred', error)
        return {
            'statusCode': 500,
            'body': json.dumps('Error occurred')
        }