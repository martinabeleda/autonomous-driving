# Lane detection using OpenCV
# Author: Martin Abeleda
# Date: 19/05/2017
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read image in color
#IMREAD_GRAYSCALE
#IMREAD_COLOR
#IMREAD_UNCHANGED
img = cv2.imread('images/2017-05-19_120235.jpg', cv2.IMREAD_COLOR)

# Extract ROI and resize
roi = img[972:1944, 0:2592]
roi = cv2.resize(roi, (800, 300))

# Filter noise
blur = cv2.GaussianBlur(roi,(15,15),0)

# Canny edge detection
edges = cv2.Canny(blur, 50, 100)



cv2.line(roi, (1296, 0), (1296, 1944), (255, 0, 0), thickness = 2)
cv2.imshow('image', roi)
cv2.imshow('canny', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
