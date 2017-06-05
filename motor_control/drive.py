import random
from datetime import datetime
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

def drive_feedback(topDisp, prevTopDisp, prevTime=datetime.now(), rightDuty, lastMove,
                   topDispCalibrate=31, yawGain=0.01, yawDerivativeGain=0.001, yawThresh=15):
    """
    Drive function.

	This function takes the angle and displacement from the `lane_detect()`
	function and controls the motors using a feedback loop in order to follow
        the lanes.
    """
    MIN_DUTY = 48
    MAX_DUTY = 150
    newRightDuty = rightDuty
	
	dt = datetime.now() - prevTime
	prevTime = datetime.now()
	errorDot = (topDisp - prevTopDisp) / dt

    if topDisp < -yawThresh and rightDuty + yawGain*topDisp + yawDerivativeGain*errorDot > MIN_DUTY: ### and lastMove is not 'decrease':
        
        # robot is angled to the left
        newRightDuty = rightDuty + yawGain*topDisp + yawDerivativeGain*errorDot
        lastMove = 'decrease'
        print 'decrease right robot yaw %f' % (newRightDuty)

    elif topDisp > yawThresh and rightDuty + yawGain*topDisp + yawDerivativeGain*errorDot < MAX_DUTY: ### and lastMove is not 'boost':
        
	    # robot is angled to the right
        newRightDuty = rightDuty + yawGain*topDisp + yawDerivativeGain*errorDot
        lastMove = 'boost'
        print 'boost right robot yaw %f' % (newRightDuty)

    else:

        # if angle > centreThresh and rightDuty + centreGain*angle < MAX_DUTY: ### and lastMove is not 'boost':
            
            # # robot is to the right of the centre line
            # newRightDuty = rightDuty + centreGain*angle
            # lastMove = 'boost'
            # print 'boost right centre %f' % (newRightDuty)

        # elif angle < -centreThresh and rightDuty + centreGain*angle > MIN_DUTY: ### and lastMove is not 'decrease':
            
            # # robot is to the left of the centre line
            # newRightDuty = rightDuty + centreGain*angle
            # lastMove = 'decrease'
            # print 'decrease right centre %f' % (newRightDuty)

        # else:
            
		# robot is close enough to the centre of the lanes
		lastMove = 'centre'
		print 'right duty is %f' % (newRightDuty)
			
	prevTopDisp = topDisp
			
    print "right duty changed by %f" % (newRightDuty - rightDuty)
    print "topDisp (yaw) %f" % (topDisp)
    #print "yaw thresh %f" % (yawThresh)
    #print "yaw gain %f" % (yawGain)
	#print "yaw derivative gain %f" % (yawDerivativeGain)
    # print "angle (centre) %f" % (angle)
    # #print "centre thresh %f" % (centreThresh)
    # #print "centre gain %f" % (centreGain)
    return newRightDuty, lastMove, prevTopDisp, prevTIme
