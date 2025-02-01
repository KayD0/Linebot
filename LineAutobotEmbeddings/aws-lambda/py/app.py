import json
import os
from botocore.exceptions import ClientError
from services.openai_service import OpenAiService
from services.cloud.aws.storage_service import StorageService

def handler(event, context):
    # リクエストボディからQAデータを取得
    try:
        body = json.loads(event['body'])
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

    # INDEX化ファイルを保存
    aws_access_key_id = os.getenv('ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('SECRET_ACCESS_KEY')
    storage_service = StorageService(
        aws_access_key_id,
        aws_secret_access_key)
    index_file_name = os.environ.get('QA_INDEX_FILE_NAME')
    qa_index_bucket_name = os.environ.get('QA_INDEX_BUCKET_NAME')
    try:
        storage_service.write_json_to_file(qa_index_bucket_name, 'qa', index_file_name, embeddings)
        return {
            'statusCode': 200,
            'body': json.dumps('INDEX化に成功しました。')
        }
    except Exception as error:
        print('S3 Write エラー')
        print('Error occurred', error)
        return {
            'statusCode': 500,
            'body': json.dumps('Error occurred')
        }