# -*- coding: utf-8 -*-
"""
 Most of this was from Adrian Rosebrock's post on pyimagesearch to figure out 
 the focal distance of my Laptop's camera.   
 https://gplinks.in/distance

Created on Wed Dec 20 12:14:18 2019

@author: Animesh
"""
# import the necessary packages
import numpy as np
import imutils
import cv2

def find_marker(image):
	# convert the image to grayscale, blur it, and detect edges
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (5, 5), 0)
	edged = cv2.Canny(gray, 35, 100)

	# find the contours in the edged image and keep the largest one;
	# we'll assume that this is our piece of paper in the image
	cnts = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	c = max(cnts, key = cv2.contourArea)
    
	# compute the bounding box of the of the paper region and return it
	return cv2.minAreaRect(c)

def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the marker to the camera
	return (knownWidth * focalLength) / perWidth

# initialize the known distance from the camera to the object, which
# in this case is 12 inches
KNOWN_DISTANCE = 12.0 

# initialize the known object width, which in this case, the piece of
# paper is 9 inches wide
KNOWN_WIDTH = 9.0 

# load the  image that contains an object that is KNOWN TO BE 1 foot from camera
# for best results, use your own captured image.
image = cv2.imread("1ft.jpg")

# find the paper marker in the image
marker = find_marker(image)

# initialize the focal length
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
print('Focal Length of camera: ', focalLength)

# compute the distance to the marker from the camera
inches = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])

# draw a bounding box around the image and display it
box = cv2.cv.BoxPoints(marker) if imutils.is_cv2() else cv2.boxPoints(marker)
box = np.int0(box)
cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

cv2.putText(image, "F=%.1f"%focalLength,
	(image.shape[1] - 200,40), cv2.FONT_HERSHEY_SIMPLEX,
	1.5, (0, 255, 0), 3)

cv2.putText(image, "%.2f ft" % (inches / 12),
	(image.shape[1] - 170, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
	1.5, (0, 255, 0), 3)

# display the image
cv2.imshow("Focal", image)
cv2.waitKey(0)

# close all windows
cv2.destroyAllWindows()