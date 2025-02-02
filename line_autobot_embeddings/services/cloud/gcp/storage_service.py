from google.cloud import storage
import json

class StorageService:
    def __init__(self):
        # Initialize Google Cloud Storage client
        self.storage_client = storage.Client()

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
                data=json.dumps(data),
                content_type='application/json'
            )
            print(f"File {file_name} written to {bucket_name}/{full_path}.")
        except Exception as e:
            print(f"Error writing file: {e}")
            raise RuntimeError('Error writing JSON file')