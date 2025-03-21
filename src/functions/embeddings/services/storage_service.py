from google.cloud import storage
import json

class StorageService:
    def __init__(self):
        # Google Cloud Storageクライアントの初期化
        self.storage_client = storage.Client()

    """
    Google Cloud StorageからJSONファイルを読み取る
    :param bucket_name: GCSバケット名
    :param path: ファイルが格納されているディレクトリのパス
    :param file_name: 読み込むファイル名
    :return: 読み込んだJSONコンテンツ
    """
    def read_json_from_file(self, bucket_name, path, file_name):
        try:
            # フルパスの生成
            full_path = f"{path}/{file_name}"
            
            # バケットとファイルの参照を取得
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(full_path)
            
            # ファイルのダウンロードとJSONとしてパース
            contents = blob.download_as_text()
            return json.loads(contents)
        except Exception as e:
            print(f"Error reading file: {e}")
            raise RuntimeError('Error reading JSON file')
    
    """
    Write a JSON object to a file in Google Cloud Storage
    :param bucket_name: GCS bucket name
    :param path: Directory path where the file will be stored
    :param file_name: Name of the file to write
    :param data: JSON data to write to the file
    """
    def write_json_to_file(self, bucket_name, path, file_name, data):
        try:
            # Generate full path
            full_path = f"{path}/{file_name}"
            
            # Get references to the bucket and blob
            bucket = self.storage_client.bucket(bucket_name)
            blob = bucket.blob(full_path)
            
            # Convert data to JSON string and upload it
            blob.upload_from_string(
                data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
                content_type='application/json'
            )
            print(f"File {file_name} written to {bucket_name}/{full_path}.")
        except Exception as e:
            print(f"Error writing file: {e}")
            raise RuntimeError('Error writing JSON file')