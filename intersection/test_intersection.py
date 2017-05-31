#imports
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

from intersection import is_red_line, read_barcode, check_light

def turn_decide(barcode):
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

	    elif choice is 'forwards': forwards(200)
