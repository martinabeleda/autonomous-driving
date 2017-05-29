import RPi.GPIO as GPIO
from time import sleep

from motors import forwards, turn_clockwise, return_to_centre, turn_anti_clockwise

GPIO.setmode(GPIO.BOARD)

motor1A = 11
motor1B = 13
motor1E = 15
motor2A = 16
motor2B = 18
motor2E = 22

GPIO.setup(motor1A, GPIO.OUT)
GPIO.setup(motor1B, GPIO.OUT)
GPIO.setup(motor1E, GPIO.OUT)
GPIO.setup(motor2A, GPIO.OUT)
GPIO.setup(motor2B, GPIO.OUT)
GPIO.setup(motor2E, GPIO.OUT)

def drive(angle, topDisplacement, centreThreshold=50, angleThreshold=5)
    """
    Drive function.

	This function takes the angle and displacement from the `lane_detect()`
	function and controls the motors in order to follow the lanes.
    """

	if angle > angleThreshold:
	    # Robot is to the right of the centre line

        turn_anti_clockwise()
        forwards()

	elif angle < -angleThreshold:
	    # Robot is to the left of the centre line

        turn_clockwise()
        forwards()

	else:
	    # Robot is close enough to the centre of the lanes
        if topDisplacement < -centreThreshold:
            # Robot is angled to the left
                
        elif topDisplacement > centreThreshold:
            # Robot is angled to the right

        else:
            # Move forward

    GPIO.cleanup()
