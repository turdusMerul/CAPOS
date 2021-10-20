import os
from os.path import getsize
from math import ceil
from datetime import datetime
import speech_recognition as SR
from pydub import AudioSegment


def tryToTranscribe():
    try:
        return str(recog.recognize_google(audio_content, language='ru'))
    except:
        tryToTranscribe()


sWorkingTime = datetime.utcnow()
print(f"[INFO] Начало обработки: {sWorkingTime}")


MAX_SEGMENT_SIZE = 10485760
OVERLAP_TIME = 500
FILE_PATH = "dataset/1.wav"
WORK_FOLDER = "dataset"
TMP_FOLDER = f"{WORK_FOLDER}/tmp"


audioFile = AudioSegment.from_file(FILE_PATH)
audioDur = len(audioFile)
fileSize = getsize(FILE_PATH)
partsNum = ceil(fileSize / MAX_SEGMENT_SIZE)
segmentDur = audioDur / partsNum

print(f"[INFO] Длительность аудиофайла: {audioDur}\n[INFO] Размер файла: {fileSize}\n[INFO] Необходимое количество сегментов: {partsNum}\n[INFO] Длина одного сегмента составит: {segmentDur}")


try:
    os.makedirs(TMP_FOLDER)
except WindowsError:
    for file in os.listdir(TMP_FOLDER):
        os.remove(f"{TMP_FOLDER}/{file}")


recog = SR.Recognizer()

result = ""
sSegmentTime = fSegmentTime = 0

for i in range(partsNum):
    sSegmentTime = fSegmentTime - (OVERLAP_TIME if fSegmentTime != 0 else 0)
    fSegmentTime += segmentDur
    audioFile[sSegmentTime:fSegmentTime].export(f"{TMP_FOLDER}/{i+1}.wav", format="wav")
    print(f"[INFO] Создан сегмент {i+1} из {partsNum}")
    
    sample_audio = SR.AudioFile(f"{TMP_FOLDER}/{i+1}.wav")
    with sample_audio as audio_file:
        audio_content = recog.record(audio_file)   
    result += tryToTranscribe()

    if i == 3: break


for file in os.listdir(TMP_FOLDER):
    os.remove(f"{TMP_FOLDER}/{file}")
os.removedirs(TMP_FOLDER)

fWorkingTime = datetime.utcnow()
print(f"[INFO] Конец обработки: {fWorkingTime}\n[INFO] На обработку затрачено: {fWorkingTime - sWorkingTime}")
print(f"[RESULT] {result}")

