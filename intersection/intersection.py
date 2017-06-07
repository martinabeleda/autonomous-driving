#import
import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy import trapz
import random
import cv2.cv as cv
import sys
import copy
import math


from datetime import datetime

def is_red_line(image):

	#crop to region of interest --> save time?? - rather than mask
        crop = image[450:600, 0:800]

	#note OpenCV represents images as NumPy arrays in reverse order - BGR
	#set limits for what is considered "red"
	#0 0 100 --> to always get all red --> or lower threshold
        #30 25 170
        #15 10 170
	red_bound_low = np.array([30,25,170])
	#230 160 255
	red_bound_high = np.array([230,160,255])
        #min G = 45
	#min B = 96
	#min R  = 150 
	#max G = 88
	#max B = 115
	#max R = 250
	

	#find red areas and apply mask
	mask = cv2.inRange(crop, red_bound_low, red_bound_high)
	red_img_crop = cv2.bitwise_and(crop,crop,mask=mask)

	#smooth the smooth
	red_img_crop = cv2.GaussianBlur(red_img_crop, (5,5), 0)

	#calculate histogram with red channel mask --> so we can see only when red is high and blue and green are low
	#range- only high levels of red
	#look at red channel
	red_hist = cv2.calcHist([crop],[2],mask,[256],[1,256])

        #plot histogram for testing
	'''
	plt.figure(1)
	plt.plot(red_hist)
	plt.xlim([1,255])
	plt.show()
        '''
	#see maximum red amount
	#find area under curve
	redH_trans = np.transpose(red_hist)

	areaHist = trapz(redH_trans, dx=1)
        print(areaHist)
        #changed 
	if areaHist[0] > 7000:
                red_flag = 1
	else:
                red_flag = 0
        #change back to red_img_crop
	return red_img_crop, red_flag

def read_barcode(cropImage):

        #blurT1 = datetime.now()
	#blurred = cv2.pyrMeanShiftFiltering(cropImage,61,91)
        #blurT2 = datetime.now()
        #print("Blur time = " + str(blurT2 - blurT1))

        #grayT1 = datetime.now()
	grayImage = cv2.cvtColor(cropImage, cv2.COLOR_BGR2GRAY)
        #grayT2 = datetime.now()

        #threshT1 = datetime.now()
	ret,thresh1 = cv2.threshold(grayImage,100,255,cv2.THRESH_BINARY_INV)
        #threshT2 = datetime.now()
        #print("thresh time = " + str(threshT2 - threshT1))

        #contT1 = datetime.now()
	contours,_ = cv2.findContours(thresh1, cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
        #contT2 = datetime.now()
        #print("contour time = " + str(contT2 - contT1))

	#remove false positives (noise) and remove red box contour
        #findCT1 = datetime.now()
	code = 0
	actual_contours = []
	for i in range(0,len(contours)):
		cnt = contours[i]
		area = cv2.contourArea(cnt)
		#comment out area print
		print("contour areas = " + str(area))
		if area > 80 and area < 500:
			code = code+1
			actual_contours.append(cnt)
	#findCT2 = datetime.now()
        #print("find actual contours time = " + str(findCT2 - findCT1))

        #moveCT1 = datetime.now()
	#add crop value to all contours (500)		
	for j in range(0,len(actual_contours)):
		for k in range(0,len(actual_contours[j])):
                        #add offset back in 
			actual_contours[j][k][0][1] = actual_contours[j][k][0][1] + 450
        #moveCT2 = datetime.now()
        #print("move drawn contour time = " + str(moveCT2 - moveCT1))
	#change back to actual_contours	only	
	return code, actual_contours

def turn_decide(barcode):
    print("turn decide");
    '''
    Turn decide function.	
    =======
    This function looks at the barcode and randomly decides on a next turn to
    make and then calls the appropriate motor function.
    '''
        
    choices = {0: ('forwards', 'right', 'left'),
               1: ('right'),
               2: ('left'),
               3: ('forwards', 'left'),
               4: ('right', 'left'),
               5: ('forwards', 'right')}
    default = 0

    if barcode > 5:
        barcode = 5

    result = choices.get(barcode, default);

    return result

def region_of_interest2(img, vertices):
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


#check light function that keeps looping till light is green 
def check_light(img):
    print("checking light")
    return_val = 0;

    #reshape
    height, width = img.shape[:2]
    I = copy.deepcopy(img[1:200, 0:width])
    masked = I
    #mask to find black
    black_bound_low = np.array([0,0,0])
    black_bound_high = np.array([100,100,100])
    mask = cv2.inRange(I, black_bound_low, black_bound_high)
	
    contours,_ = cv2.findContours(mask, cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
    counter = 0;
    rect = []
    for i in range(0,len(contours)):
	cnt = contours[i]
	peri = cv2.arcLength(cnt, True)
	approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
	if len(approx) == 4:
                (x, y, w, h) = cv2.boundingRect(approx)
		rect_area = h*w;
		if(rect_area > 700 and rect_area < 2000):
			rect.append(cv2.boundingRect(approx))
			cv2.rectangle(I,(x,y),(x+w,y+h),(255,0,0),3)
			lowerLeftPoint = [x,y+h]
			upperLeftPoint = [x,y]
			upperRightPoint = [x+w,y]
			lowerRightPoint = [x+w,y+h]
			pts = np.array([[lowerLeftPoint, upperLeftPoint,upperRightPoint, lowerRightPoint]], dtype=np.int32)
			masked = region_of_interest2(I,pts)
			counter = counter +1
			
    cimg = cv2.cvtColor(masked,cv2.COLOR_BGR2GRAY)
    ret,thresh1 = cv2.threshold(cimg,200,255,cv2.THRESH_BINARY)
    cirles_draw = []
    circles = cv2.HoughCircles(thresh1, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100, param1=10,param2=10,minRadius=4,maxRadius=32)

    if circles is not None and counter > 0:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # loop over the (x, y) coordinates and radius of the circles
            for (a, b, r) in circles:
                for j in range(0,counter):
                    (x, y, w, h) = rect[j];
                    if(x < a < x+w and y < b < y+h):
                            print("Ligh t is On")
                            # should it just be return_val = 1?
                            return_val = return_val + 1;
                            cv2.circle(I,(a,b),r,(0,0,255),2);
                            cirles_draw.append((a, b, r))
	
    return I,rect,cirles_draw,return_val; 
