# Lane detection using OpenCV on Raspberry Pi
# Author: Martin Abeleda
# Date: 19/05/2017
import atexit
import time
import cv2
import numpy as np
import os
cmd = 'sudo pigpiod'
os.system(cmd)
import warnings
import pigpio

from picamera.array import PiRGBArray
from picamera import PiCamera
from datetime import datetime
from motor_control.drive import drive_feedback, turn_decide
from motor_control.motors import motor_setup, calibrate_motors, stop
from lane_follow.lane_detect import lane_detect
from lane_follow.calibrate_camera import calibrate_camera
from intersection.intersection import is_red_line, read_barcode, check_light, turn_decide

pi = pigpio.pi()

# stop motors on exit
def exit_handler():
    stop()
    cv2.destroyAllWindows()

atexit.register(exit_handler)

# ignore polyfit rank warnings
warnings.simplefilter('ignore', np.RankWarning)

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (800, 608)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(800, 608))
camera.vflip = True
camera.hflip = True

# Red flag
RED = 1
NOT_RED = 0

# Display defines
DISPLAY = 1
font = cv2.FONT_HERSHEY_PLAIN
fontSize = 2
green = [0,255,0]
red = [0,0,255]

# Camera calibration
#topDispCalibrate, angleCalibrate = calibrate_camera(camera)
#print "topDispCalibrate = %f, angleCalibrate = %f" % (topDispCalibrate, angleCalibrate)

# Motor Calibration
leftDuty = 65
rightDuty = calibrate_motors(leftDuty)
lastMove = 'centre'

# Camera Calibration
yawThresh = 30
topDispCalibrate=33.17
topDispMax = 50


# wait for user to say GO
print "Waiting for you to press g"
while(1):
    inkey = raw_input()
    if inkey is "g": break

motor_setup()

# allow the camera to warmup
time.sleep(1)

# main loop

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    try:

        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array
        start = datetime.now()

        # gaussian blur
        kernelSize = 5
        blur = cv2.GaussianBlur(image, (kernelSize,kernelSize), 0)

        # check if we are at the red line
        maskedImage, line = is_red_line(image)

        if line is RED:

            print("RED LINE!!!")
            stop()
	    turnCode,barcode_contours = read_barcode(maskedImage)
	    print("Turn Code", turnCode)
	    #Move forwards

	    print("Move Forwards")
            if DISPLAY:
	        cv2.putText(image,'Red Line 20cm Away',(25,25), font, fontSize, green,2)
	        cv2.putText(image,'Barcode = '+ str(turnCode),(25,100), font, fontSize, green ,2)
		cv2.drawContours(image,barcode_contours,-1,(0,255,0),2)
        else:
            # detect lanes in the image
            (img, angle, topDisp, bottomDisp) = lane_detect(blur)

            topDisp = topDisp - topDispCalibrate

            # execute lane following algorithm
            drive_feedback(topDisp, rightDuty, leftDuty, yawThresh)  ###

        runtime = datetime.now() - start
        fps = round(1/runtime.total_seconds(), 1)

        #color = [0, 255, 0]
        #cv2.putText(img, str(fps) + "FPS", (0, 30), font, fontSize, color)
        if DISPLAY:
            cv2.line(image,(0,450),(800,450), red, 2)
        cv2.imshow('Main Frame', image)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
	#if key == ord("q"):
	#    break

        #  clear the stream in preparation for the next frame
        rawCapture.truncate(0)

    except KeyboardInterrupt:
        stop()
