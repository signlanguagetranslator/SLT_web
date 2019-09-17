from flask import Flask, request
from flask_cors import CORS
import tensorflow as tf
import base64
import json
import cv2
import time
import numpy as np

modelFullPath = './output_graph.pb'
labelsFullPath = './output_labels.txt'

# cross 해결
app = Flask(__name__)
cors = CORS(app, resources={
  r"/*": {"origin": "*"},
})

# TENSOR 준비
sess = tf.Session()
with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

boundaries = [
    ([160, 83, 80], [180, 255, 255])
]

def handsegment(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower, upper = boundaries[0]
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")
    mask = cv2.inRange(frame, lower, upper)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    output = cv2.bitwise_and(mask, frame)
    # show the images
    return output

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/Wakeword',  methods=['POST'])
def WakeWord():
    print( "/getImage  <- ")

    
    image = request.get_json()['image'].split(',')
    image = base64.decodestring(bytes((image[0:])[1],'utf-8'))
    image = np.fromstring(image,dtype=np.uint8)
    imagePath = "./image/imageToSave.jpeg"

    with open(imagePath, "wb") as fh:
        fh.write(image)

    if not tf.gfile.Exists(imagePath):
        tf.logging.fatal('File does not exist %s', imagePath)
        jsonresult = {
            'result': None
        }
        resJson = json.dumps(jsonresult)
        print("/getImage  ->")
        print(resJson)
        return resJson

    f = open(labelsFullPath, 'rb')
    lines = f.readlines()
    labels = [str(w).replace("\n", "") for w in lines]
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    start = time.time()
    frame = cv2.imread(imagePath)
    frame = handsegment(frame)
    cv2.imwrite('./image/currnet.jpg',frame)
    image_data = tf.gfile.FastGFile('./image/currnet.jpg', 'rb').read()
    predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data })
    predictions = np.squeeze(predictions)
    top_k = predictions.argsort()[-5:][::-1]  # 가장 높은 확률을 가진 5개(top 5)의 예측값(predictions)을 얻는다.#
    answer = labels[top_k[0]]

    print("ans : " + str(answer))
    print("time : ", time.time()-start)


    jsonresult = {
        'result' : answer
    }
    resJson = json.dumps(jsonresult)
    print("/getImage  ->")
    print(resJson)
    return resJson




if __name__ == '__main__':
    app.run(host='localhost', port = 5000, debug = True)

