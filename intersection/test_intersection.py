#imports
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

from intersection import is_red_line, read_barcode, check_light

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

# Main loop
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    	# grab the raw NumPy array representing the image, then initialize the timestamp
		# and occupied/unoccupied text
		image = frame.array

		# gaussian blur
	    kernelSize = 5
	    blur = cv2.GaussianBlur(gray, (kernelSize,kernelSize), 0)

		#Check to see  if red line is present - enter intersection module 
		maskedImage, line = is_red_line(image)

		if line is RED:

			#if at intersection 
			turnCode = read_barcode(maskedImage)
			print("Turn Code", turnCode)

			#Move forwards
			print("Move Forwards")

			#wait and exit on green light
			check_light()
			print("Light is green")

			turn_decide(turnCode)

		else
			print("Not an intersection")


		# show the frame
		cv2.imshow("Frame", img)
    	key = cv2.waitKey(1) & 0xFF

		# clear the stream in preparation for the next frame
		rawCapture.truncate(0)

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break




def turn_decide(barcode):
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
    result = choices.get(barcode, default)

    if result is 'right': right_turn()

    elif result is 'left': left_turn()

    else:
        # make a random choice
        choice = random.choice(result)

    	if choice is 'right': right_turn()

	    elif choice is 'left': left_turn()

	    elif choice is 'forwards': forwards(200)
