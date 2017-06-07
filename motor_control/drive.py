import random
from datetime import datetime
from time import sleep
from motors import straight, left, right

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

def drive_feedback(rightDuty, leftDuty, topDisp, topDispThresh, angle, angleThresh, 
                   sleepAngleLeft, sleepTopDispLeft, sleepAngleRight, sleepTopDispRight, sleepStraight):
    """
    Drive function.

	This function takes the angle and displacement from the `lane_detect()`
	function and controls the motors using a feedback loop in orSder to follow
        the lanes.
    """
    if topDisp > topDispThresh:

        # robot is on the right
        left(rightDuty)
        sleep(sleepTopDispLeft)
        straight(leftDuty,rightDuty)
        sleep(sleepStraight)
        print "Turn Left topDisp"

    elif topDisp < -topDispThresh:
        # robot is on the left

        right(leftDuty)
        sleep(sleepTopDispRight)
        straight(leftDuty,rightDuty)
        sleep(sleepStraight)
        print "Turn Right topDisp"
    else:
        if angle < -angleThresh:
        
            # robot is angled to the left
            right(leftDuty)
            sleep(sleepAngleRight)
            straight(leftDuty,rightDuty)
            sleep(sleepStraight)
            print "Turn Right angle"
        elif angle > angleThresh:
        
	    # robot is angled to the right
            left(rightDuty)
            sleep(sleepAngleLeft)
            straight(leftDuty,rightDuty)
            sleep(sleepStraight)
            print "Turn Left angle"
        else:
            
	    # robot is close enough to the centre of the lanes
            straight(leftDuty,rightDuty)
