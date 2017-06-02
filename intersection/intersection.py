#import
import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy import trapz

from datetime import datetime


def is_red_line(image):

	#crop to region of interest --> save time?? - rather than mask
	crop = image[500:600, 0:800]

	#note OpenCV represents images as NumPy arrays in reverse order - BGR
	#set limits for what is considered "red"
	#0 0 100 --> to always get all red --> or lower threshold
	red_bound_low = np.array([0,0,120])
	red_bound_high =np.array([130,130,255])

	#find red areas and apply mask
	mask = cv2.inRange(crop, red_bound_low, red_bound_high)
	red_img_crop = cv2.bitwise_and(crop,crop,mask=mask)

	#calculate histogram with red channel mask --> so we can see only when red is high and blue and green are low
	#range- only high levels of red
	#look at red channel
	red_hist = cv2.calcHist([crop],[2],mask,[256],[1,256])

	#see maximum red amount
	#find area under curve
	redH_trans = np.transpose(red_hist)

	areaHist = trapz(redH_trans, dx=1)

	if areaHist[0] > 12000:
    	print("Red detected") 
	else:
    	print("NOT AN INTERSECTION")

	return red_img_crop, red_flag


def read_barcode(maskedImage):

	#potentially do this before hand if rest of code works with 9,9 kernel
	maskedImage = cv2.GaussianBlur(maskedImage, (9,9),0)
	blurred = cv2.pyrMeanShiftFiltering(maskedImage,51,91)

	grayImage = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
	ret,thresh1 = cv2.threshold(grayImage,70,255,cv2.THRESH_BINARY_INV)

	contours,_ = cv2.findContours(thresh1, cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

	#remove false positives (noise) and remove red box contour
	code = 0
	for i in range(0,len(contours)):
		cnt = contours[i]
		area = cv2.contourArea(cnt)
		if area > 20 and area < 3000:
			code = code+1

	return code

def check_light():
	print("checking light")

	
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
    result = choices.get(barcode, default);

    if(result is 'right'):
        right_turn();
    elif(result is 'left'):
        left_turn();
    else:
        # make a random choice
        choice = random.choice(result)

    	if choice is 'right': right_turn()

	    elif choice is 'left': left_turn()

	    elif choice is 'forwards': forwards(200) 


