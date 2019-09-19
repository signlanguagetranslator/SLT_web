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
    print( "/Wakeword  <- ")

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
    print("/Wakeword  ->")
    print(resJson)
    return resJson

@app.route('/SaveImage',  methods=['POST'])
def Saveimage():
    print( "/SaveImage  <- ")
    image = request.get_json()['image'].split(',')
    image = base64.decodestring(bytes((image[0:])[1],'utf-8'))
    fileName = str(request.get_json()['fileName'])
    image = np.fromstring(image,dtype=np.uint8)
    imagePath = "./image/" + fileName + ".jpeg"

    with open(imagePath, "wb") as fh:
        fh.write(image)

    frame = cv2.imread(imagePath)
    frame = handsegment(frame)
    cv2.imwrite('./masking/candy/'+fileName + '.jpg', frame)
    jsonresult = {
        'result' : True
    }
    resJson = json.dumps(jsonresult)
    print("/SaveImage  ->")
    print(resJson)
    return resJson

@app.route('/Predict',  methods=['GET'])
def Predict():
    print( "/Predict  <- ")
    start = time.time()
    word = signRecognition('./masking')
    
    # for i in glob.glob("./masking/candy/*.jpg"):
    #     os.remove(i)
    
    # for i in glob.glob("./image/*.jpeg"):
    #     os.remove(i)
    jsonresult = {
        'word' : word
    }
    resJson = json.dumps(jsonresult)
    print("/Predict  ->")
    print(resJson)
    print(time.time()-start)
    return resJson

if __name__ == '__main__':
    app.run(host='localhost', port = 5000, debug = True)

