import argparse
import os
from papago import translate
import csv
import json
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "../../../google_api.json"


def transcribe_model_selection_gcs(file_name, gcs_uri, model):
    """Transcribe the given audio file asynchronously with
    the selected model."""
    from google.cloud import speech
    client = speech.SpeechClient()

    audio = speech.types.RecognitionAudio(uri=gcs_uri)

    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        # sample_rate_hertz=16000,
        language_code='ko-KR',
        model=model,
        enable_automatic_punctuation=True,
        enable_separate_recognition_per_channel=True,
    )

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result()
    print('operation completed')
    for i, result in enumerate(response.results):
        
        line = result.alternatives[0].transcript
        
        for stc in divide_stc(line):
            print(stc)
            if len(stc)!=0:
                with open(f'{file_name}.csv', 'a') as f:
                    writer = csv.writer(f)
                    
                    stc = stc+'.'
                    writer.writerow([stc])
                    writer.writerow([translate(stc)])
            
    
def divide_stc(line):
    return line.split('.')

