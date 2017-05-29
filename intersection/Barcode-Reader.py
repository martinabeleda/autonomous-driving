import cv2
import cv2.cv as cv
import numpy as np
import sys
from math import log10, floor
import math
from datetime import datetime
from scipy import ndimage

#find angle between corners of square to make sure its a square
def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

#detect squares
def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)#was 5
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    if max_cos < 0.25:
                        squares.append(cnt)
    return squares

#find area of square
def PolygonArea(corners):
    n = len(corners) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += corners[i][0] * corners[j][1]
        area -= corners[j][0] * corners[i][1]
    area = abs(area) / 2.0
    return area

def centeroidnp(arr):
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return sum_x/length, sum_y/length

def roundup(x):
    return int(math.floor(x / 10.0)) * 10

def main(imageName):
	#Read Image
	img = cv2.imread(imageName)

	img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# lower mask (0-10)
	lower_red = np.array([0,50,50])
	upper_red = np.array([10,255,255])
	mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

	# upper mask (170-180)
	lower_red = np.array([170,50,50])
	upper_red = np.array([180,255,255])
	mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

	# join my masks
	mask = mask0+mask1

	# set my output img to zero everywhere except my mask
	output_img = img.copy()
	output_img[np.where(mask==0)] = 0

	#Rotate the Image 
	angle = 270
	rotated = ndimage.rotate(output_img, angle)

	#Turn back to BGR
	img_bgr=cv2.cvtColor(rotated, cv2.COLOR_HSV2BGR)

	#Turn BW
	img_bw = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY);
	squares = find_squares(img_bw)

	first = 0;
	dist_array = []
	squares2 = []

	# if area is less than a certain amount
	# get a list of all the centroids and then get the distances between each centroid
	for i in range(0,len(squares)):
		area = PolygonArea(squares[i])
		if area < 30000:
			centroid = centeroidnp(squares[i])
			squares2.append(squares[i])
			if first == 0:
				prev_point = centeroidnp(squares[i]);		
				first = 1;

			cur_point = centeroidnp(squares[i]);
			dist = math.hypot(prev_point[0] - cur_point[0], prev_point[1] - cur_point[1])
			dist_array.append(roundup(dist))
		
	mylist = list(set(dist_array))
	print(mylist)

	k =0;
	#Get unique components out of the list and draw (this section is not nessesary)
	'''
	for i in range(0,len(squares2)):
		if (dist_array[i] == mylist[k] and k+1 <= len(mylist)):
			k = k +1;
			pts = squares2[i].reshape((-1,1,2))
			cv2.polylines(img_bgr,[pts],True,(0,0,255),4)
			print("Found.")
		if k+1 > len(mylist):
			break
	'''

	#Write the image (this section is not nessesary)
	#cv2.imwrite('./kekking2.png',img_bgr) 

	#Print Number of Barcodes
	print(len(mylist))



if __name__ == "__main__":
	imageName = sys.argv[1];
	main(imageName)
