# Lane detection using OpenCV on Raspberry Pi
# Author: Martin Abeleda
# Date: 19/05/2017
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

from motor_control.drive import drive_feedback, turn_decide
from motor_control.motors import motor_setup, forwards, turn_clockwise
from lane_follow.lane_detect import lane_detect
from intersection.intersection import is_red_line, read_barcode, check_light

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (800, 600)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(800, 600))
camera.vflip = True
camera.hflip = True

RED = 1
leftDuty = 160
rightDuty = calibrate_motors(leftDuty)

# allow the camera to warmup
time.sleep(0.1)

# main loop
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array

	# gaussian blur
	kernelSize = 5
	blur = cv2.GaussianBlur(gray, (kernelSize,kernelSize), 0)

	# check if we are at the red line
	masked, line = is_red_line(blur)

    if line is RED:

	    print "red"
"""
            # display raw input
	    img = image

	    # store the number of barcode lines
	    barcode = read_barcode(masked)

	    # move forwards to the line
	    forwards_hard(leftDuty, distance=200)

	    # wait for the light to turn green
	    check_light()


	    # execute a random turn based on barcode
	    turn_decide(barcode)

"""
    else:

		# detect lanes in the image
		(img, angle, topDisplacement, bottomDisplacement) = lane_detect(blur)

		# execute lane following algorithm
		rightDuty = drive_feedback(angle, topDisplacement, leftDuty, rightDuty)

	# show the frame
	cv2.imshow("Frame", img)
    	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
	    break
