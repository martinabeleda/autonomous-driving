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

#Debbug flags so i dont have to keep commenting and uncommenting
DEBUG_REDLINE = 1
DEBUG_HISTOGRAM = 0
DEBUG_HUE = 0
HUE_MASK = 0

#other defines
CROP = 450
MIN_BARCODE_AREA = 80 
MAX_BARCODE_AREA = 400
# should be 6000
MIN_RED_AREA = 5000
DAYTIME = 1

def is_red_line(image):

	#crop to region of interest --> save time?? - rather than mask
        crop = image[CROP:600, 0:800]

       
        #adjust brightness
        # jokes maybe try staurdate image instead ---> intensify colour    
        hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        hsv[:,:,1] += 20
        

        #try using hue to mask
        #HSV - h --> range from 0 - 360 represents a color
        # s - colour intensity - 0 -100
        # v - brightness - 0 -100
        if HUE_MASK:
            crop = hsv    
            red_bound_low = np.array([0,0,0])
	    #230 160 255
	    red_bound_high = np.array([360,100,100])         
                
        #using RGB mask instead
        else:

            #convert image back to RGB 
            crop = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
	    #note OpenCV represents images as NumPy arrays in reverse order - BGR
	    #set limits for what is considered "red"
	    #0 0 100 --> to always get all red --> or lower threshold
            #30 25 170
            #15 10 170
            if DAYTIME:
                red_bound_low = np.array([0,0,130])
	        #230 160 255
	        red_bound_high = np.array([170,110,255])
            #night time    
	    else:   
                red_bound_low = np.array([30,25,170])
	        #230 160 255
	        red_bound_high = np.array([230,160,255])    
                #min G = 45
                #min B = 96
                #min R  = 150 
                #max G = 88
                #max B = 115
                #max R = 250

	#smooth the smooth
	crop = cv2.GaussianBlur(crop, (5,5), 0)
	
	#find red areas and apply mask
	mask = cv2.inRange(crop, red_bound_low, red_bound_high)
	if HUE_MASK:
            crop = cv2.cvtColor(crop, cv2.COLOR_HSV2BGR)
	red_img_crop = cv2.bitwise_and(crop,crop,mask=mask)
        
	#calculate histogram with red channel mask --> so we can see only when red is high and blue and green are low
	#range- only high levels of red
	#look at red channel
	red_hist = cv2.calcHist([crop],[2],mask,[256],[1,256])

        if DEBUG_HISTOGRAM:
            #plot histogram for testing
	    
	    plt.figure(1)
	    plt.plot(red_hist)
	    plt.xlim([1,255])
	    plt.show()
            
	#see maximum red amount
	#find area under curve
	redH_trans = np.transpose(red_hist)

	areaHist = trapz(redH_trans, dx=1)
	if DEBUG_REDLINE:
            print("Area of Red Line = " + str(areaHist))
        #changed 
	if areaHist[0] > MIN_RED_AREA:
                red_flag = 1
	else:
                red_flag = 0
        if DEBUG_HUE:
            return crop, red_flag
        else:
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

        # Remove false negatives
        #kernel = np.ones((5, 5), np.uint8)
        #thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_CLOSE, kernel)
        
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
		#debug
		if DEBUG_REDLINE:
                    print("contour areas = " + str(area))
		if area > MIN_BARCODE_AREA and area < MAX_BARCODE_AREA:
			code = code+1
			actual_contours.append(cnt)
	#findCT2 = datetime.now()
        #print("find actual contours time = " + str(findCT2 - findCT1))

        #moveCT1 = datetime.now()
	#add crop value to all contours (500)		
	for j in range(0,len(actual_contours)):
		for k in range(0,len(actual_contours[j])):
                        #add offset back in
                        if DEBUG_REDLINE:
			    actual_contours[j][k][0][1] = actual_contours[j][k][0][1]
			else:
                            actual_contours[j][k][0][1] = actual_contours[j][k][0][1] + CROP        
        #moveCT2 = datetime.now()
        #print("move drawn contour time = " + str(moveCT2 - moveCT1))
	#change back to actual_contours	only
	return code, actual_contours, contours

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
		#maybs change from 700 to 400 from riley 
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
