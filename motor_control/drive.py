import random
from time import sleep
from motors import forwards_lane_follow, right_turn, left_turn, forwards_hard

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

def drive_feedback(angle, topDisp, rightDuty, lastMove, angleCalibrate=5.16, topDispCalibrate=31,
                   yawGain=0.01, yawThresh=15,
                   centreGain=1, centreThresh=10):
    """
    Drive function.

	This function takes the angle and displacement from the `lane_detect()`
	function and controls the motors using a feedback loop in order to follow
        the lanes.
    """
    MIN_DUTY = 48
    MAX_DUTY = 150
    newRightDuty = rightDuty

    topDisp = topDisp - topDispCalibrate
    angle = angle - angleCalibrate
    
	# once gains are tuned, check that we need this
    if angle > 45:
        angle = 45
    elif angle < -45:
        angle = -45

    if topDisp > 100:
        topDisp = 100
    elif topDisp < -100:
        topDisp = -100

    if topDisp < -yawThresh and rightDuty + yawGain*topDisp > MIN_DUTY: ### and lastMove is not 'decrease':
        
        # robot is angled to the left
        newRightDuty = rightDuty + yawGain*topDisp
        lastMove = 'decrease'
        print 'decrease right robot yaw %f' % (newRightDuty)

    elif topDisp > yawThresh and rightDuty + yawGain*topDisp < MAX_DUTY: ### and lastMove is not 'boost':
        
	    # robot is angled to the right
        newRightDuty = rightDuty + yawGain*topDisp
        lastMove = 'boost'
        print 'boost right robot yaw %f' % (newRightDuty)

    else:

        if angle > centreThresh and rightDuty + centreGain*angle < MAX_DUTY: ### and lastMove is not 'boost':
            
            # robot is to the right of the centre line
            newRightDuty = rightDuty + centreGain*angle
            lastMove = 'boost'
            print 'boost right centre %f' % (newRightDuty)

        elif angle < -centreThresh and rightDuty + centreGain*angle > MIN_DUTY: ### and lastMove is not 'decrease':
            
            # robot is to the left of the centre line
            newRightDuty = rightDuty + centreGain*angle
            lastMove = 'decrease'
            print 'decrease right centre %f' % (newRightDuty)

        else:
            
            # robot is close enough to the centre of the lanes
            lastMove = 'centre'
            print 'right duty is %f' % (newRightDuty)
			
    print "right duty changed by %f" % (newRightDuty - rightDuty)
    print "topDisp (yaw) %f" % (topDisp)
    print "yaw thresh %f" % (yawThresh)
    print "yaw gain %f" % (yawGain)
    print "angle (centre) %f" % (angle)
    print "centre thresh %f" % (centreThresh)
    print "centre gain %f" % (centreGain)
    return newRightDuty, lastMove
