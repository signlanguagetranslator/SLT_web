# -*- coding: utf-8 -*-

"""Inception v3 architecture 모델을 retraining한 모델을 이용해서 이미지에 대한 추론(inference)을 진행하는 예제"""

import cognitive_face as CF
import numpy as np

KEY = '9b3e66f7f6db4361b2e1073ed554a5f9'
CF.Key.set(KEY)
BASE_URL = 'https://faceapi125.cognitiveservices.azure.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)






# 프레임마다 실행
def faceDetection(imagePath, DetectFaceSnd, cntEmo, facelist):
    faces = CF.face.detect(imagePath, face_id=False, attributes='emotion')
    #print(faces)
    # 표정 평균내기.
    maxEmo = 0
    maxVal = 0
    sndVal = 0
    sndEmo = 0
    for face in faces:
        emotion = face['faceAttributes']['emotion']
        i = 0
        for emo in face['faceAttributes']['emotion']:
            if DetectFaceSnd == False:
                if i == 7:
                    DetectFaceSnd = True
                facelist[i] = emo
            val = emotion[emo]
            if maxVal < val:
                sndVal = maxVal
                sndEmo = maxEmo
                maxEmo = i
                maxVal = val
            i += 1

        if maxEmo == 'neutral' and sndVal > 0.1:
            maxEmo = sndEmo

        cntEmo[maxEmo] += 1
        maxVal = 0
    return cntEmo, facelist

# 문장 인식 전에 마지막으로 한 번 실행
def FinalEmotion(Directory):
    cntEmo = np.zeros(8, dtype=int)
    facelist = ['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']
    cntEmo, facelist = faceDetection(Directory + '1.jpeg', False, cntEmo, facelist)
    cntEmo, facelist = faceDetection(Directory + '5.jpeg', True, cntEmo, facelist)
    cntEmo, facelist = faceDetection(Directory + '9.jpeg', True, cntEmo, facelist)
    cntEmo, facelist = faceDetection(Directory + '13.jpeg', True, cntEmo, facelist)
    cntEmo, facelist = faceDetection(Directory + '17.jpeg', True, cntEmo,facelist)
    cntEmo, facelist = faceDetection(Directory + '21.jpeg', True, cntEmo, facelist)
    cntEmo, facelist = faceDetection(Directory + '25.jpeg', True, cntEmo, facelist)
    
    #print(cntEmo)
    maxVal = 0
    res = 'anger'
    i = 0
    
    for k in cntEmo:
        if maxVal < k:
            maxVal = k
            res = facelist[i]
        i += 1
    
    print(res)
    return res


def TranswithEmotion(string, Emotion):
    wordarray = ['', '', '', '', '']
    index = 0
    wordidx = 0
    while string.find(' ',index)!= -1:
        preidx = index
        index = string.find(' ', index)
        wordarray[wordidx] = string[preidx:index]
        index += 1
        wordidx +=1

    wordarray[wordidx] = string[index:]

    if Emotion == 'surprise':

        if wordarray[0] == 'son':
            if wordidx >= 1 and (wordarray[1] == 'buy' or wordarray[1] == 'call' or wordarray[1] =='dance' or wordarray[1] =='find' or wordarray[1] == 'help'):
                wordarray[0] = 'did son'
            elif wordidx >= 1:
                wordarray[0] = 'is son'

        elif (wordarray[0] == 'where' or wordarray[0] == 'what') and wordidx >= 1:
            if wordarray[1] == 'time' or wordarray[1] == 'date':
                wordarray[1] += ' is it'
            else:
                wordarray[1] = 'is ' + wordarray[1]

        wordarray[wordidx] += '?'

    elif Emotion != 'neutral':
        wordarray[wordidx] += '!'


    result = ''
    for i in range(0, wordidx + 1):
        result += wordarray[i] + ' '

    return result