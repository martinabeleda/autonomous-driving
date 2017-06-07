import os
cmd = 'sudo pigpiod'
os.system(cmd)
import pigpio

from motors import motors_setup, turn_clockwise, turn_anti_clockwise

pi = pigpio.pi()

# Motor Calibration
leftDuty = 100
rightDuty = calibrate_motors(leftDuty)
SPEED = 100 # mm/s
TURN_RATE = 200 # degs/s

turn_anti_clockwise(TURN_RATE,3600)
stop()