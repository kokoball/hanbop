# 모듈 로딩 후 오디오 추출
import moviepy.editor as mp
from pydub import AudioSegment
import sys

def extract_wav(file_name):
    clip = mp.VideoFileClip(f"./src/mp4/{file_name}.mp4")
    clip.audio.write_audiofile(f"./src/wav/{file_name}.wav")

    sound = AudioSegment.from_wav(f"./src/wav/{file_name}.wav")
    sound = sound.set_channels(1)
    sound.export(f"./src/mono_wav/{file_name}.wav", format="wav")


if __name__ == '__main__':
    extract_wav(
        file_name=sys.argv[1]
    )