import cv2
import cv2.cv as cv
import numpy as np
import sys
import copy
import math
from datetime import datetime

startTime = datetime.now()

imageName = sys.argv[1];

img = cv2.imread(imageName)
height, width = img.shape[:2]

I = copy.deepcopy(img[1:1000, 1000:width]) # Crop from x, y, w, h -> 100, 200, 300, 400
u = copy.deepcopy(img[1:1000, 1000:width])
# NOTE: its img[y: y + h, x: x + w] and *not* img[x: x + w, y: y + h]

height, width = I.shape[:2]

for i in range(0,height-1):
    for j in range(0,width-1):
        if I[i,j,0] < 70 and I[i,j,1] < 70   and I[i,j,2] < 70:
            I[i,j,0] = 0;
            I[i,j,1] = 0;
            I[i,j,2] = 0;
        else:
            I[i,j,0] = 255;
            I[i,j,1] = 255;
            I[i,j,2] = 255;
 
blurred = cv2.GaussianBlur(I, (5, 5), 0)
thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

img_grey = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY);


circles = cv2.HoughCircles(img_grey,cv.CV_HOUGH_GRADIENT,5,20,param1=50,param2=100,minRadius=10,maxRadius=40);

# Create a blank 300x300 black image
image = np.zeros((height, width, 3), np.uint8)
# Fill image with red color(set each pixel to red)
image[:] = (0, 0, 0)

circles = np.uint16(np.around(circles,decimals=0))
for i in circles[0,:]:
    #total = 0;
    #count = 0;
    mask = copy.deepcopy(np.zeros(u.shape, np.uint8));
    center = (i[0], i[1]);
    radius = i[2];

    cv2.circle(mask, center, radius, 255, -1)
    where = np.where(mask == 255)
    intensity_values_from_original = img[where[1], where[0]]
    if np.median(intensity_values_from_original) > 120:
        cv2.circle(u,(i[0],i[1]),i[2],(255,255,255),2);

print datetime.now() - startTime
cv2.imwrite('./kekking2.png',u) 

