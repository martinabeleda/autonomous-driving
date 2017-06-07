# Lane detection using OpenCV on Raspberry Pi Author: Martin Abeleda Date: 19/05/2017
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
from motor_control.motors import motor_setup, calibrate_motors, forwards, turn_clockwise, turn_anti_clockwise, stop
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

# Red and green flags
RED = 0
GREEN = 0

# robot states
LANE_FOLLOW = 0
TO_INTERSECTION = 1
CHECKING_LIGHT = 2
THROUGH_INTERSECTION = 3
state = LANE_FOLLOW

# Display defines
DISPLAY = 0
font = cv2.FONT_HERSHEY_PLAIN
fontSize = 2
green = [0,255,0]
red = [0,0,255]

# Camera Calibration
topDispCalibrate = 40
angleCalibrate = 0
#topDispCalibrate, angleCalibrate = calibrate_camera(camera)
#print "topDispCalibrate = %f, angleCalibrate = %f" % (topDispCalibrate, angleCalibrate)
topDispThresh = 30
angleThresh = 2

# Motor Calibration
leftDuty = 170
rightDutyInit = 182
rightDuty = calibrate_motors(leftDuty, rightDutyInit)
lastMove = 'centre'
SPEED = 100 # mm/s
TURN_RATE = 200 # degs/s
sleepAngleLeft = 0.1
sleepTopDispLeft = 0.17
sleepAngleRight = 0.05
sleepTopDispRight = 0.20
sleepStraight = 0.05

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
		
		# if lane following
		if state is LANE_FOLLOW:
		
		    print "Lane following."
		
		    # detect lanes in the image
            (image, angle, topDisp, bottomDisp) = lane_detect(blur)

			# apply camera calibration to output
            topDisp = topDisp - topDispCalibrate
            angle = angle - angleCalibrate
		
            # execute lane following algorithm
            drive_feedback(rightDuty, leftDuty, topDisp, topDispThresh, angle, angleThresh,
                           sleepAngleLeft, sleepTopDispLeft, sleepAngleRight, sleepTopDispRight, sleepStraight)
						   
			# check if we see the red line
            maskedImage, line = is_red_line(blur)
			if line is RED:
			
			    # check the time
				t1 = datetime.now()
				
				print "Red line detected."
				
	            turnCode,barcode_contours = read_barcode(maskedImage)
				
	            print("Turn Code", turnCode)
				
			    # Change state: Drive to the intersection
				state = TO_INTERSECTION
		
		elif state is TO_INTERSECTION:
		
		    print "Driving to intersection (hard-coded)"
			
			# lane follow for 150 mm
		    driveTime = datetime.now() - t1
            if driveTime.total_seconds() < 150 / SPEED:
			    # detect lanes in the image
                (image, angle, topDisp, bottomDisp) = lane_detect(blur)

			    # apply camera calibration to output
                topDisp = topDisp - topDispCalibrate
                angle = angle - angleCalibrate

                # execute lane following algorithm
                drive_feedback(rightDuty, leftDuty, topDisp, topDispThresh, angle, angleThresh)
			
			# then change state to check the light if there is a light else execute manoeuvre
		    else:
			    if turnCode < 2:
				    state = THROUGH_INTERSECTION
			    else:
				    stop()
			        state = CHECKING_LIGHT
			else:
			    
		
		elif state is CHECKING_LIGHT:
		    
			print "Checking light"
		    
			# check the light
		    trafficlight_image,rect,cirles_draw, traffic_code, = get_trafficlights(image)
			
			# if it's green, change state to execute manoeuvre
		    if traffic_code is GREEN:
			
			    print "Light turned green."
			    # check the time
				t1 = datetime.now()
				
			    state = THROUGH_INTERSECTION
								
			# otherwise, stay still
			else:
			    stop()
		
		elif state is DRIVING_INTERSECTION:
		    driveTime = datetime.now() - t1
			
            action = turn_decide(turnCode)
			
			if action is 'forwards':
			    print "Forwards"
			    forwards(leftDuty, rightDuty, SPEED, 250)
				state = LANE_FOLLOW
			
			elif action is 'left':
			    print "Left turn"
			    forwards(leftDuty, rightDuty, SPEED, 190)
				turn_anti_clockwise(TURN_RATE, 90)
				state = LANE_FOLLOW
			
			elif action is 'right':
			    print "Right turn"
			    forwards(leftDuty, rightDuty, SPEED, 350)
				turn_clockwise(TURN_RATE, 90)
				state = LANE_FOLLOW
	
        if DISPLAY:
	    runtime = datetime.now() - start
            fps = round(1/runtime.total_seconds(), 1)
            cv2.putText(img, str(fps) + "FPS", (0, 30), font, fontSize, [0, 255, 0])	
	    
            cv2.line(image,(0,450),(800,450), red, 2)
	
            cv2.imshow('Main Frame', image)
            key = cv2.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
	    if key == ord("q"):
	        break

        #  clear the stream in preparation for the next frame
        rawCapture.truncate(0)

    except KeyboardInterrupt:
        stop()
