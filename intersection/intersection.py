#import
import cv2
import numpy as np
import matplotlib.pyplot as plt
from numpy import trapz
import random

from datetime import datetime

def is_red_line(image):

	#crop to region of interest --> save time?? - rather than mask
        crop = image[450:600, 0:800]

        #add contrast - jks takes 10 seconds
        '''
        contT1 = datetime.now()
        crop = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)
        crop[:,:,2] = [[max(pixel - 25,0) if pixel < 190 else min (pixel + 25,255) for pixel in row] for row in crop[:,:,2]]
        crop = cv2.cvtColor(crop, cv2.COLOR_HSV2BGR)
        contT2 = datetime.now()
        print("contrast time =" + str(contT2 - contT1))
        '''
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
	return code, actual_contours, contours, grayImage

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

    if barcode > 5:
        barcode = 5

    result = choices.get(barcode, default);

    if result is 'right':
        #right_turn();
        print("Choice = Right")
    elif result is 'left':
        #left_turn();
        print("Choice = Left")
    else:
        # make a random choice
        choice = random.choice(result)

    	if choice is 'right': 
    	    #right_turn()
    	    print("Choice = Right")

	elif choice is 'left': 
	    #left_turn()
	    print("Choice = Left")
	elif choice is 'forwards': 
	    #forwards(200) 
	    print("Choice = Straight")
