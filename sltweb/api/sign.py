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

import handsegment as hsx
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

net = get_network_wide(25, 2048, 29)
model = tflearn.DNN(net, tensorboard_verbose=0)

try:
    model.load('checkpoints/pool.model')
    print("\nModel Exists! Loading it")
    print("Model Loaded")
except Exception:
    print("\nNo previous checkpoints of %s exist" % ('pool.model'))
    print("Exiting..")
    sys.exit()

def signRecognition(imagePath):
    # frames라는 폴더에 있는 파일들을 읽어서 결과를 냄.
    predictions = ps.predict_on_frames(imagePath, 'retrained_graph.pb', 'Placeholder',
                                            "module_apply_default/InceptionV3/Logits/GlobalPool", 25)
    out_file = 'predicted-frames-test.pkl'
    with open(out_file, 'wb') as fout:
        pickle.dump(predictions, fout)
    res = re.eval_video(out_file, 25, 25, signlabels, model)
    return res

if __name__ == '__main__':
    faceDetection('face.jpg')
#    print(facelist)
#    FinalEmotion()