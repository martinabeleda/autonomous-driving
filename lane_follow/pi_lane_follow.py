# Lane detection using OpenCV on Raspberry Pi
# Author: Martin Abeleda
# Date: 19/05/2017
import io
import picamera
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt

#Create a memory stream so photos doesn't need to be saved in a file
stream = io.BytesIO()

#Get the picture (low resolution, so it should be quite fast)
#Here you can also specify other parameters (e.g.:rotate the image)
with picamera.PiCamera() as camera:
    camera.resolution = (800, 600)
    camera.capture(stream, format='jpeg')

#Convert the picture into a numpy array
buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

#Now creates an OpenCV image
img = cv2.imdecode(buff, 1)

# Detect lanes and draw on `img`
(detected, lines, angle, displacement) = lane_detect(img)

print angle
print displacement

# Display
cv2.imshow('image', detected)
cv2.imshow('masked w/ lines', lines)
