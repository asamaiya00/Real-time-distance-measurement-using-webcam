# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 14:53:09 2019

@author: Animesh
"""
import cv2
#import numpy as np

focal = 450.0 #focal length of  camera

width = 8.0 #width of object

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0) #capture from webcam

def calculate_distance(width, focal, perWidth):
    return (width * focal) / perWidth

while True:
    ret,img = cap.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        new_distance = calculate_distance(width,focal,w)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
        print(new_distance /12 , " ft")
    
    img = cv2.resize(img,(int(img.shape[1]*2),int(img.shape[0]*2)))
    cv2.putText(img, "%.2fft"%(new_distance/12),
	(img.shape[1] - 210, img.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
		1.5, (0, 255, 0), 3)
    cv2.imshow("img",img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows( )
