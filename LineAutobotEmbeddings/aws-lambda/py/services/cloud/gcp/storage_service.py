import json
import boto3
import logging
from botocore.exceptions import ClientError

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        # Amazon S3クライアントの初期化
        # 認証情報を明示的に指定
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key)

    async def write_json_to_file(self, bucket_name, path, file_name, data):
        """
        Writes a JSON object to a file in AWS S3
        :param bucket_name: The name of the S3 bucket.
        :param path: The path to the directory where the file will be stored.
        :param file_name: The name of the file to be written.
        :param data: The JSON object to write.
        """
        try:
            full_path = f"{path}/{file_name}"
            json_data = json.dumps(data, indent=2)
            
            self.s3.put_object(
                Bucket=bucket_name,
                Key=full_path,
                Body=json_data,
                ContentType='application/json'
            )
            
            print(f"File {full_path} written to bucket {bucket_name}.")
        except ClientError as e:
            print(f"Error writing file: {e}")
            raise Exception("Error writing JSON file")