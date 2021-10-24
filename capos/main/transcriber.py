import io
from os import path
from math import ceil
import speech_recognition as SR
from pydub import AudioSegment


recog = SR.Recognizer()


def tryToTranscribe(audio_content, trying = 0):
    try:
        return str(recog.recognize_google(audio_content, language='ru'))
    except:
        if trying == 2: return " [ ДАННЫЙ УЧАСТОК ТРАНСКРИБИРОВАТЬ НЕ УДАЛОСЬ ] "
        print(f"[INFO] Попытка {trying+2}")
        tryToTranscribe(audio_content, trying + 1)


def transcribe(file_path):
    MAX_SEGMENT_SIZE = 10485760
    OVERLAP_TIME = 500

    audioFile = AudioSegment.from_file(file_path, format=file_path.split(".")[1])
    audioDur = len(audioFile)
    fileSize = path.getsize(file_path)
    partsNum = ceil(fileSize / MAX_SEGMENT_SIZE)
    segmentDur = audioDur / partsNum
    sSegmentTime = fSegmentTime = 0
    result = ""

    for i in range(partsNum):
        sSegmentTime = fSegmentTime - (OVERLAP_TIME if fSegmentTime != 0 else 0)
        fSegmentTime += segmentDur
        bytes = io.BytesIO()
        audioFile[sSegmentTime:fSegmentTime].export(bytes, format="wav")
        bytes.seek(0)
        with SR.AudioFile(bytes) as source:
            audio_content = recog.record(source)
        resp = tryToTranscribe(audio_content)
        result += " " + (resp if resp else "___")

    return(result)