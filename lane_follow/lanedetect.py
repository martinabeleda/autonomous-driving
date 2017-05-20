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
#img = cv2.imread('images/2017-05-19_120425.jpg', cv2.IMREAD_COLOR)

# Extract ROI and resize
roi = img[972:1944, 0:2592]
roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
img = cv2.resize(img, (800, 600))
roi = cv2.resize(roi, (800, 300))

# Line Detection
blur = cv2.GaussianBlur(roi,(5,5),0)
edges = cv2.Canny(blur, threshold1=100, threshold2=200)
minLineLength = 30
maxLineGap = 10
lines = cv2.HoughLinesP(edges, 1, np.pi/180, 40, minLineLength, maxLineGap)

# Display hough lines
for x in range(0, len(lines)):
    for x1,y1,x2,y2 in lines[x]:
        cv2.line(img,(x1,y1+300),(x2,y2+300),(0,255,0), thickness=2)

# Display center line
#cv2.line(img, (1296, 0), (1296, 1944), (255, 0, 0), thickness=2)
cv2.line(img, (400, 0), (400, 600), (255, 0, 0), thickness=2)

# Display
cv2.imshow('image', img)
cv2.imshow('canny', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
