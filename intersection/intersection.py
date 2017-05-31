#import
import cv2
import numpy as np 
import matplotlib.pyplot as plt 

from datetime import datetime 

from region_of_interest import region_of_interest


def is_red_line(image)

	#crop to region of interest --> save time?? - rather than mask
	crop = image[500:600, 0:800]

	#note OpenCV represents images as NumPy arrays in reverse order - BGR
	#set limits for what is considered "red"
	#0 0 100 --> to always get all red --> or lower threshold 
	red_bound_low = np.array([0,0,120])
	red_bound_high =np.array([115,115,255])

	#find red areas and apply mask
	mask = cv2.inRange(crop, red_bound_low, red_bound_high)
	red_img_crop = cv2.bitwise_and(crop,crop,mask=mask)

	#calculate histogram with red channel mask --> so we can see only when red is high and blue and green are low 
	#range- only high levels of red 
	#look at red channel 
	red_hist = cv2.calcHist([crop],[2],mask,[256],[1,256])

	#see maximum red amount 
	#or can change mask red values and do a for loop --> depends how time consuming that is 
	amount_of_red = np.amax(red_hist)

	if amount_of_red > 450:
	    red_flag = 1
	else:
	    red_flag = 0

	return red_img_crop, red_flag


def read_barcode(maskedImage)



def check_light()
