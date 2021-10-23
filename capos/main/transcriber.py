from os.path import getsize
from math import ceil
import speech_recognition as SR
from pydub import AudioSegment
import io


recog = SR.Recognizer()


def tryToTranscribe(audio_content):
    try:
        return str(recog.recognize_google(audio_content, language='ru'))
    except:
        tryToTranscribe(audio_content)


def transcribe(file_path):
    print(f"[INFO] File path is: {file_path}")
    MAX_SEGMENT_SIZE = 10485760
    OVERLAP_TIME = 500


    audioFile = AudioSegment.from_file(file_path)
    audioDur = len(audioFile)
    fileSize = getsize(file_path)
    partsNum = ceil(fileSize / MAX_SEGMENT_SIZE)
    segmentDur = audioDur / partsNum
    sSegmentTime = fSegmentTime = 0
    result = ""

    for i in range(partsNum):
        sSegmentTime = fSegmentTime - (OVERLAP_TIME if fSegmentTime != 0 else 0)
        fSegmentTime += segmentDur
        bytes = io.BytesIO()
        audioFile[sSegmentTime:fSegmentTime].export(bytes, format="wav")
        print(f"[INFO] Сегмент {i}/{partsNum} выделен")
        bytes.seek(0)
        with SR.AudioFile(bytes) as source:
            audio_content = recog.record(source)
        result += tryToTranscribe(audio_content)
        print(f"[INFO] Сегмент {i}/{partsNum} транскрибирован")

        if i == 3: break
    return(result)

if __name__ == "__main__":
    print(transcribe("dataset/1.wav"))