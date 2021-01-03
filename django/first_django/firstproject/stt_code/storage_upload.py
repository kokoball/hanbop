
import sys

# [START storage_upload_file]
from google.cloud import storage

import os
from google.cloud.bigquery.client import Client

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "../../../google_api.json"
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


# [END storage_upload_file]

if __name__ == "__main__":
    file_name = 'gp'
    file_path = f'./src/mono_wav/{file_name}.wav'
    upload_blob(
        bucket_name='my_fisrt_ko',
        source_file_name=file_path,
        destination_blob_name=file_name
    )