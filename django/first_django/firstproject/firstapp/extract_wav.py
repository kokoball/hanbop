
# 모듈 로딩 후 오디오 추출
import moviepy.editor as mp
from pydub import AudioSegment
import sys


def extract_wav(file_path):
    file_name = file_path.split('\\')[-1].split('.')[0]
    path_to_media = file_path.split(file_name)[0]

    
    
    clip = mp.VideoFileClip(file_path)
    
    clip.audio.write_audiofile(path_to_media+f"{file_name}.wav")

    sound = AudioSegment.from_wav(path_to_media+f"{file_name}.wav")
    sound = sound.set_channels(1)
    sound.export(path_to_media+f"{file_name}.wav", format="wav")

    return path_to_media+f"{file_name}.wav"

if __name__ == '__main__':
    extract_wav(
        file_name=sys.argv[1]
    )