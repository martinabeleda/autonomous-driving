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
from motor_control.motors import motor_setup, calibrate_motors, forwards_hard, forwards_lane_follow, stop
from lane_follow.lane_detect import lane_detect
from lane_follow.calibrate_camera import calibrate_camera
from intersection.intersection import is_red_line

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
camera.resolution = (800, 600)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(800, 600))
camera.vflip = True
camera.hflip = True

# Red flag
RED = 1
NOT_RED = 0

# Camera calibration
topDispCalibrate, angleCalibrate = calibrate_camera()
#topDispCalibrate=42.54
#angleCalibrate=1.808021636
print "topDispCalibrate = %f, angleCalibrate = %f" % (topDispCalibrate, angleCalibrate)

# Motor Calibration
leftDuty = 70
rightDuty = calibrate_motors(leftDuty)
lastMove = 'centre'

# Camera Calibration
centreThresh=10
centreGain = 0.03
yawThresh = 25
yawGain=0.01
#topDispCalibrate=42.54
#angleCalibrate=1.808021636
topDispMax = 80
angleMax = 45


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
        #masked, line = is_red_line(blur)

        line = NOT_RED
        if line is RED:

            img = blur
            print "red"
            """
            # display raw input
            img = image

            # store the number of barcode lines
            barcode = read_barcode(masked)

            # move forwards to the line
            forwards_hard(leftDuty, rightDuty, distance=200)

            # wait for the light to turn green
            check_light()

            # execute a random turn based on barcode
            turn_decide(leftDuty, barcode)
            """
        else:
            # detect lanes in the image
            (img, angle, topDisp, bottomDisp) = lane_detect(blur)

            topDisp = topDisp - topDispCalibrate
            angle = angle - angleCalibrate

            # Set upper and lower bounds for angle and topDisplacement
            # once gains are tuned, check that we need this
            if angle > angleMax:
                angle = angleMax
            elif angle < -angleMax:
                angle = -angleMax

            if topDisp > topDispMax:
                topDisp = topDispMax
            elif topDisp < -topDispMax:
                topDisp = -topDispMax

	    #while 1:
		#print "type a - centreGain, s - centreThresh, d - yawGain, f - yawThresh, g - angleCalibrate, h - topDispCalibrate, or n"
	        #inkey = raw_input()
	        #if inkey is "a": centreGain = float(raw_input("set centreGain to "))
		#elif inkey is "s": centreThresh = float(raw_input("set centreThresh to "))
		#elif inkey is "d": yawGain = float(raw_input("set yawGain to "))
		#elif inkey is "f": yawThresh = float(raw_input("set yawThresh to "))
		#elif inkey is "g": angleCalibrate = float(raw_input("set angleCalibrate to "))
		#elif inkey is "h": topDispCalibrate = float(raw_input("set topDispCalibrate to "))
                #elif inkey is "n": break

            # execute lane following algorithm
            rightDuty, lastMove = drive_feedback(angle, topDisp, rightDuty, lastMove, angleCalibrate, topDispCalibrate,
                                                 yawGain, yawThresh, centreGain, centreThresh)  ###

            forwards_lane_follow(leftDuty, rightDuty)

        runtime = datetime.now() - start
        fps = round(1/runtime.total_seconds(), 1)

        font = cv2.FONT_HERSHEY_PLAIN
        fontSize = 3
        color = [0, 255, 0]
        cv2.putText(img, str(fps) + "FPS", (0, 30), font, fontSize, color)
        cv2.imshow('Main Frame', img)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
	if key == ord("q"):
	    break

        #  clear the stream in preparation for the next frame
        rawCapture.truncate(0)

    except KeyboardInterrupt:
        stop()
