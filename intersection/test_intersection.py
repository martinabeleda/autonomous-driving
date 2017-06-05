#imports
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
from datetime import datetime

from intersection import is_red_line, read_barcode, check_light, turn_decide

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (800, 600)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(800, 600))
camera.vflip = True
camera.hflip = True

# allow the camera to warmup
time.sleep(0.1)

#defines
RED = 1
DISPLAY = 1
font = cv2.FONT_HERSHEY_PLAIN
fontsize = 2
green = [0,255,0]
red = [0,0,255]

cv2.namedWindow('Main Frame', cv2.WINDOW_NORMAL)
# Main loop
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    	# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
		image = frame.array
            
		# gaussian blur
	    	kernelSize = 5
	    	blur = cv2.GaussianBlur(image, (kernelSize,kernelSize), 0)

		#Check to see  if red line is present - enter intersection module 
		redLineT1 = datetime.now()
		maskedImage, line = is_red_line(image)
		redLineT2 = datetime.now()
		print("red line time = "+ str(redLineT2 - redLineT1))

		if line is RED:
			print("RED LINE!!!")
			#if at intersection 
			barCodeT1 = datetime.now()
			turnCode,barcode_contours = read_barcode(maskedImage)
			barCodeT2 = datetime.now()
			print("Barcode reading time = " + str(barCodeT2-barCodeT1))
			print("Turn Code", turnCode)
			#Move forwards
			print("Move Forwards")

			#wait and exit on green light
			check_light()
			print("Light is green")

			turn_decide(turnCode)
			if DISPLAY:
				displayT1 = datetime.now()
				cv2.putText(image,'Red Line 20cm Away',(25,25), font, fontsize, green,2)
				cv2.putText(image,'Barcode = '+ str(turnCode),(25,100), font, fontsize, green ,2)
				cv2.drawContours(image,barcode_contours,-1,(0,255,0),2)
				displayT2 = datetime.now()
				print("Display time = " + str(displayT2 - displayT1))
		else:
			print("Not an intersection")
			#delay frame rate - maybs remove?
			if DISPLAY:
				cv2.putText(image,'Not an Intersection',(25,25), font, fontsize, green, 2)
			time.sleep(0.1)


		# show the frame
		# display all data to screen 
		if DISPLAY:
			cv2.line(image,(0,540),(800,540),red,2)
        
		cv2.imshow('Main Frame', image)
                key = cv2.waitKey(1) & 0xFF

		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			cv2.destroyAllWindows()
			break




