import numpy as np
import tensorflow as tf
import cv2
import handsegment as hs

import time

modelFullPath = './output_graph.pb'                                      # 읽어들일 graph 파일 경로
labelsFullPath = './output_labels.txt'                                   # 읽어들일 labels 파일 경로

# TENSOR 준비
sess = tf.Session()
with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')
softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

f = open(labelsFullPath, 'rb')
lines = f.readlines()
labels = [str(w).replace("\n", "") for w in lines]

def wakeWordDetection(imagePath):
    print("imagePath : " + imagePath)
    answer = None    
    # read Label File


    start = time.time()
    # Masking
    frame = cv2.imread(imagePath+".jpeg")
    frame = hs.handsegment(frame)
    print("CHK")
    cv2.imwrite(imagePath+".jpg" , frame)
    image_data = tf.gfile.FastGFile(imagePath+".jpg", 'rb').read()

    # Predict
    predictions = sess.run(softmax_tensor,{'DecodeJpeg/contents:0': image_data })
    predictions = np.squeeze(predictions)
    top_k = predictions.argsort()[-5:][::-1]
    answer = labels[top_k[0]]
    
    print("ans : " + str(answer))
    print("time : ", time.time()-start)
    return str(answer)
