#import RPi.GPIO as GPIO
import random
from time import sleep

from motors import forwards_lane_follow, right_turn, left_turn, forwards_hard


#GPIO.setmode(GPIO.BOARD)

motor1A = 11
motor1B = 13
motor1E = 15
motor2A = 16
motor2B = 18
motor2E = 22

"""
GPIO.setup(motor1A, GPIO.OUT)
GPIO.setup(motor1B, GPIO.OUT)
GPIO.setup(motor1E, GPIO.OUT)
GPIO.setup(motor2A, GPIO.OUT)
GPIO.setup(motor2B, GPIO.OUT)
GPIO.setup(motor2E, GPIO.OUT)
"""

def turn_decide(dcL, barcode):
    """
    Turn decide function.

    This function looks at the barcode and randomly decides on a next turn to
    make and then calls the appropriate motor function.
    """

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

	elif choice is 'forwards': forwards_hard(leftDuty, rightDuty, 210)

def drive_feedback(angle, topDisplacement, rightDuty, leftDuty, lastMove, angleGain, displacementGain, angleThreshMin, angleThreshMax, centreThreshMin, centreThreshMax):
    """
    Drive function.

	This function takes the angle and displacement from the `lane_detect()`
	function and controls the motors using a feedback loop in order to follow
    the lanes.
    """
    MIN_DUTY = 48
    MAX_DUTY = 100
    newRightDuty = rightDuty

    if topDisplacement < centreThreshMin and rightDuty + displacementGain*topDisplacement > MIN_DUTY: ###and lastMove is not 'decrease':
        # robot is angled to the left
        # calculate angle
        #angle = abs(topDisplacement/2)
        #turn_clockwise(angle)
        newRightDuty = rightDuty + displacementGain*topDisplacement
        lastMove = 'decrease'
        print 'decrease right robot angle %f' % (newRightDuty)

    elif topDisplacement > centreThreshMax and rightDuty + displacementGain*topDisplacement < MAX_DUTY: ###and lastMove is not 'boost':
	# robot is angled to the right
        # calculate angle
        #angle = topDisplacement/2
        #turn_anti_clockwise(angle)
        newRightDuty = rightDuty + displacementGain*topDisplacement
        lastMove = 'boost'
        print 'boost right robot angle %f' % (newRightDuty)

    else:

        if angle > angleThreshMax and rightDuty + angleGain*angle < MAX_DUTY: ### and lastMove is not 'boost':
            # robot is to the right of the centre line
            # increase rightDuty
            newRightDuty = rightDuty + angleGain*angle
            lastMove = 'boost'
            print 'boost right centre %f' % (newRightDuty)

        elif angle < angleThreshMin and rightDuty + angleGain*angle > MIN_DUTY: ### and lastMove is not 'decrease':
            # robot is to the left of the centre line
            # decrease rightDuty
            newRightDuty = rightDuty + angleGain*angle
            lastMove = 'decrease'
            print 'decrease right centre %f' % (newRightDuty)

        else:
            # robot is close enough to the centre of the lanes
            lastMove = 'centre'
            print 'right duty is %f' % (newRightDuty)
    print "right duty changed by %f" % (newRightDuty - rightDuty)
    print "topDisplacement %f" % (topDisplacement)
    print "centre thresh min %f" % (centreThreshMin)
    print "centre thresh max %f" % (centreThreshMax)
    print "displacement gain %f" % (displacementGain)
    print "angle %f" % (angle)
    print "angle thresh min %f" % (angleThreshMin)
    print "angle thresh max %f" % (angleThreshMax)
    print "angle gain %f" % (angleGain)
    return newRightDuty, lastMove
