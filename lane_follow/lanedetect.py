# Lane detection using OpenCV
# Author: Martin Abeleda
# Date: 19/05/2017
import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
Applies an image mask.

Only keeps the region of the image defined by the polygon
formed from `vertices`. The rest of the image is set to black.
"""
def region_of_interest(img, vertices):

    #defining a blank mask to start with
    mask = np.zeros_like(img)

    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

# Read image in color
#IMREAD_GRAYSCALE
#IMREAD_COLOR
#IMREAD_UNCHANGED
img = cv2.imread('images/2017-05-19_120235.jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('images/2017-05-19_120425.jpg', cv2.IMREAD_COLOR)

# Resize and convert to grayscale
img = cv2.resize(img, (800, 600))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Gaussian Blur
kernelSize = 5
blur = cv2.GaussianBlur(gray, (kernelSize,kernelSize), 0)

# Canny Edge Detection
lowThreshold = 150
highThreshold = 200
edges = cv2.Canny(blur, lowThreshold, highThreshold)

# Extract Region of Interest
lowerLeftPoint = [0, 600]
middleLeftPoint = [0, 450]
upperLeftPoint = [250, 300]
upperRightPoint = [550, 300]
middleRightPoint = [800, 450]
lowerRightPoint = [800, 600]
pts = np.array([[lowerLeftPoint, middleLeftPoint, upperLeftPoint, upperRightPoint, middleRightPoint, lowerRightPoint]], dtype=np.int32)
roi = region_of_interest(edges, pts)

# Hough Lines
rho = 1
theta = np.pi/180
threshold = 30
minLineLength = 20
maxLineGap = 20
lines = cv2.HoughLinesP(roi, rho, theta, threshold, minLineLength, maxLineGap)

# Display hough lines
for x in range(0, len(lines)):
    for x1,y1,x2,y2 in lines[x]:
        cv2.line(img,(x1,y1+300),(x2,y2+300),(0,255,0), thickness=2)

# Display center line
#cv2.line(img, (1296, 0), (1296, 1944), (255, 0, 0), thickness=2)
cv2.line(img, (400, 0), (400, 600), (255, 0, 0), thickness=2)

# Display
cv2.imshow('image', roi)
cv2.imshow('canny', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
