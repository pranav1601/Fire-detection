# -*- coding: utf-8 -*-
"""
Created on Wed Jan  9 03:30:51 2019

@author: Pranav
"""

# import the necessary packages
from imutils import contours
from skimage import measure
import numpy as np
import argparse
import imutils
import cv2
import pyaudio  
import wave 
import os
 #filename=enter filename
# construct the argument parse and parse the arguments
cap = cv2.VideoCapture(filename)
while(True):
    # Capture frame-by-frame
    ret, image = cap.read()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (11, 11), 0)
    
    thresh = cv2.threshold(blurred, 200, 255, cv2.THRESH_BINARY)[1]
    
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=4)
    
    labels = measure.label(thresh, neighbors=8, background=0)
    mask = np.zeros(thresh.shape, dtype="uint8")
     
    # loop over the unique components
    for label in np.unique(labels):
    	# if this is the background label, ignore it
    	if label == 0:
    		continue
     
    	# otherwise, construct the label mask and count the
    	# number of pixels 
    	labelMask = np.zeros(thresh.shape, dtype="uint8")
    	labelMask[labels == label] = 255
    	numPixels = cv2.countNonZero(labelMask)
     
    	# if the number of pixels in the component is sufficiently
    	# large, then add it to our mask of "large blobs"
    	if numPixels > 300:
    		mask = cv2.add(mask, labelMask)
            
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
  #  cnts = contours.sort_contours(cnts)[0]
     
    # loop over the contours
    for (i, c) in enumerate(cnts):
    	# draw the bright spot on the image
    	(x, y, w, h) = cv2.boundingRect(c)
    	((cX, cY), radius) = cv2.minEnclosingCircle(c)
    	cv2.circle(image, (int(cX), int(cY)), int(radius),
    		(0, 255, 0), 3)
    	cv2.putText(image, "#{}".format(i + 1), (x, y - 15),
    		cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 2)
        
    
# show the output image
    cv2.imshow("Image", image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()