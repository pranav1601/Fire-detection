# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 01:49:40 2019

@author: Pranav
"""

from keras.models import load_model
import cv2
import numpy as np
from subprocess import Popen
import math

#filename=enter filename
count = 0
videoFile = filename
cap = cv2.VideoCapture(videoFile)
frameRate = cap.get(5) #frame rate
x=1
while(cap.isOpened()):
    frameId = cap.get(1) #current frame number
    ret, frame = cap.read()
    if (ret != True):
        break
    if (frameId % math.floor(frameRate) == 0):
        filename ="test%d.jpg" % count;count+=1
        cv2.imwrite(filename, frame)
    cv2.imshow("Image", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
print ("Done!")
cv2.destroyAllWindows()
model = load_model('ip.h5')



predictlist=[]

for i in range(5):
    
    filename='test'+str(i)+'.jpg'
    img = cv2.imread(filename)
    img = cv2.resize(img,(320,240))
    img = np.reshape(img,[1,320,240,3])
    
    classes = model.predict_classes(img)
    predictlist.append(classes[0][0])
    
if(predictlist.count(1)>predictlist.count(0)):
    Popen('python siren.py')
    Popen('python contour.py')
else:
    print('no fire')
    
