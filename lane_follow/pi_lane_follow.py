# Lane detection using OpenCV on Raspberry Pi
# Author: Martin Abeleda
# Date: 19/05/2017
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt

from lane_detect import lane_detect

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.1)

# grab an image from the camera
camera.capture(rawCapture, format="bgr")
image = rawCapture.array

# display the image on screen and wait for a keypress
cv2.imshow("Image", image)
cv2.waitKey(0)

# Detect lanes and draw on `img`
#(detected, lines, angle, displacement) = lane_detect(img)

#print angle
#print displacement

# Display
# cv2.imshow('region', roi)
#cv2.imshow('image', img)
#cv2.imshow('masked w/ lines', lines)
