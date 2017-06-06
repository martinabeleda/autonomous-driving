import cv2
import cv2.cv as cv
import numpy as np
import sys
import copy
import math
from datetime import datetime

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """

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

	
def get_trafficlights(imageName):
	return_val = 0;

	#reshape
	height, width = img.shape[:2]
	I = copy.deepcopy(img[1:600, 1000:width])

	#mask to find black
	black_bound_low = np.array([0,0,0])
	black_bound_high = np.array([100,100,100])
	mask = cv2.inRange(I, black_bound_low, black_bound_high)
	
	contours,_ = cv2.findContours(mask, cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
	for i in range(0,len(contours)):
		cnt = contours[i]
		peri = cv2.arcLength(cnt, True)
		approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
		if len(approx) == 4:
			(x, y, w, h) = cv2.boundingRect(approx)
			rect_area = h*w;
			if(rect_area > 2000 and rect_area < 15000):
				rect = cv2.boundingRect(approx)
				cv2.rectangle(I,(x,y),(x+w,y+h),(255,0,0),3)
				lowerLeftPoint = [x,y+h]
				upperLeftPoint = [x,y]
				upperRightPoint = [x+w,y]
				lowerRightPoint = [x+w,y+h]
				pts = np.array([[lowerLeftPoint, upperLeftPoint,upperRightPoint, lowerRightPoint]], dtype=np.int32)
				masked = region_of_interest(I,pts)
			
	cimg = cv2.cvtColor(masked,cv2.COLOR_BGR2GRAY)
	ret,thresh1 = cv2.threshold(cimg,200,255,cv2.THRESH_BINARY)

	circles = cv2.HoughCircles(thresh1, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100, param1=10,param2=10,minRadius=4,maxRadius=32)
	if circles is not None:
		# convert the (x, y) coordinates and radius of the circles to integers
		circles = np.round(circles[0, :]).astype("int")

		# loop over the (x, y) coordinates and radius of the circles
		for (a, b, r) in circles:
			(x, y, w, h) = rect;
			if(x < a < x+w and y < b < y+h):
				print("Light is On")
				return_val = 1;
				cv2.circle(I,(a,b),r,(0,0,255),2);
	
	return return_val;
	#cv2.imwrite('./output.png',thresh1) 
	#cv2.imwrite('./output1.png',I ) 
