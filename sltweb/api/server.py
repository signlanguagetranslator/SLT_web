from flask import Flask, request
from flask_cors import CORS
import tensorflow as tf
import base64
import json
import cv2
import time
import numpy as np
import glob 
import os

from sign import signRecognition
from Wakeword import wakeWordDetection
from handsegment import handsegment
from chat import detect_intent_texts
from Emotion import FinalEmotion, TranswithEmotion

# cross 해결
app = Flask(__name__)
cors = CORS(app, resources={
  r"/*": {"origin": "*"},
})

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/Wakeword',  methods=['POST'])
def WakeWord():
    image = request.get_json()['image']
    if( image == None):
        resJson = json.dumps({'result' : False})
        return resJson
    image = image.split(',')
    image = base64.decodestring(bytes((image[0:])[1],'utf-8'))
    image = np.fromstring(image,dtype=np.uint8)
    imagePath = "./image/imageToSave"

    with open(imagePath+".jpeg", "wb") as fh:
        fh.write(image)
    start = time.time()
    answer = wakeWordDetection(imagePath)
    print(time.time()-start)
    print(answer)
    jsonresult = {
        'result' : answer
    }
    resJson = json.dumps(jsonresult)
    print(resJson)
    return resJson

@app.route('/SaveImage',  methods=['POST'])
def Saveimage():
    image = request.get_json()['image'].split(',')
    image = base64.decodestring(bytes((image[0:])[1],'utf-8'))
    fileName = str(request.get_json()['fileName'])
    print(fileName)
    if(int( fileName) > 25):
        jsonresult = {
            'result' : False
        }
        resJson = json.dumps(jsonresult)
        return resJson
    image = np.fromstring(image,dtype=np.uint8)
    imagePath = "./image/" + fileName + ".jpeg"

    with open(imagePath, "wb") as fh:
        fh.write(image)

    frame = cv2.imread(imagePath)
    frame = handsegment(frame)
    frame = cv2.resize(frame, dsize=(1920, 1080), interpolation=cv2.INTER_AREA)
    cv2.imwrite('./masking/candy/'+fileName + '.jpg', frame)
    jsonresult = {
        'result' : True
    }
    resJson = json.dumps(jsonresult)
    print(resJson)
    return resJson

@app.route('/Predict',  methods=['POST'])
def Predict():
    start = time.time()
    print(request.get_json())
    emotion = request.get_json()['emotion']

    if emotion == "":
        emotion = FinalEmotion('./image/')
    word = signRecognition('./masking')
    jsonresult = {
        'word' : word,
        'emotion': emotion
    }
    
    resJson = json.dumps(jsonresult)
    print(resJson)
    print(time.time()-start)
    return resJson


@app.route('/Chat',  methods=['POST'])
def Chat():
    start = time.time()
    sentence = request.get_json()['sentence']
    emotion = request.get_json()['emotion']
    sentence = TranswithEmotion(sentence, emotion)
    ans = detect_intent_texts('restobot-441ff', '16080fa56f1a4da9950a2b26c04e4d31', sentence, 'en')
    jsonresult = {
        'response' : ans,
        'sentence' : sentence
    }
    resJson = json.dumps(jsonresult)
    print(resJson)
    print(time.time()-start)
    return resJson


if __name__ == '__main__':
    app.run(host='localhost', port = 5000, debug = True)

