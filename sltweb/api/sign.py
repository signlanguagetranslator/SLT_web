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
