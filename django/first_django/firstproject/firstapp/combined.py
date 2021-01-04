from .extract_wav import extract_wav
from .storage_upload import upload_blob
from .video_transcripts import transcribe_model_selection_gcs
import argparse


# file_name = 'ted1'
# file_path = f'./src/mono_wav/{file_name}.wav'
# gs_uri = f'gs://bucket_name/{file_name}'

def combined(file_name, file_path, gs_uri):
    path_to_wav = extract_wav(file_path)
    path_to_mediadir = path_to_wav.split(file_name)[0]

    print('########extract_wav completed')

    upload_blob(bucket_name='my_first_ko2', source_file_name=path_to_wav, destination_blob_name=file_name)
    
    print('########upload to storage completed')

    transcribe_model_selection_gcs(path_to_mediadir, file_name, gs_uri, 'video')