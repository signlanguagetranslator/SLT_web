# -*- coding: utf-8 -*-

"""Inception v3 architecture 모델을 retraining한 모델을 이용해서 이미지에 대한 추론(inference)을 진행하는 예제"""

import cognitive_face as CF
import numpy as np
import tensorflow as tf
import cv2
import time
import pickle
import tflearn
import sys

import handsegment as hs
import rnn_eval as re
import predict_spatial as ps
from rnn_utils import get_network_wide, get_data

signlabels = re.load_labels('retrained_labels.txt')
KEY = '9b3e66f7f6db4361b2e1073ed554a5f9'
CF.Key.set(KEY)
BASE_URL = 'https://faceapi125.cognitiveservices.azure.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)
cntEmo = np.zeros(8, dtype=int)

facelist = ['anger', 'contempt', 'disgust', 'fear', 'happiness', 'neutral', 'sadness', 'surprise']

DetectFaceSnd = False

def faceDetection(imagePath):
    faces = CF.face.detect(imagePath, face_id=False, attributes='emotion')
    print(faces)
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
                    face_emo = True
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

def FinalEmotion():
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
