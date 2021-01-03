import argparse
import os
from .papago import translate
from .kakao import eng2kor
import csv
import json
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/ko/Oasis-hackathon/team8_hackathon/django/google_api.json"

from .models import FileUpload
from google.cloud import speech


def transcribe_model_selection_gcs(path_to_mediadir, file_name, gcs_uri, model):
    """Transcribe the given audio file asynchronously with
    the selected model."""
    
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        #sample_rate_hertz=16000,
        language_code="ko-KR",
        model=model,
        enable_automatic_punctuation=True,
        enable_separate_recognition_per_channel=True,
    )

    operation = client.long_running_recognize(request={"config":config, "audio":audio})

    print('Waiting for operation to complete...')
    response = operation.result()
    print('operation completed')
    for i, result in enumerate(response.results):
        
        line = result.alternatives[0].transcript
        
        for stc in divide_stc(line):
            print(stc)
            if len(stc)!=0:
                with open(path_to_mediadir+f'{file_name}_스크립트.csv', 'a') as f:
                    writer = csv.writer(f)
                    
                    stc = stc+'.'
                    writer.writerow([stc])
                    #writer.writerow([eng2kor(stc)])
    

    
def divide_stc(line):
    return line.split('.')

