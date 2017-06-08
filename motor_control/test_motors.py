import os
cmd = 'sudo pigpiod'
os.system(cmd)
import pigpio

from motors import motor_setup, turn_clockwise, turn_anti_clockwise, calibrate_motors, forwards, stop

pi = pigpio.pi()

# Motor Calibration
SPEED = 215 # mm/s
TURN_RATE = 180 # degs/s
leftDuty = 120
rightDutyInit = 147.2
#rightDuty = calibrate_motors(leftDuty, rightDutyInit)
#rightDuty = rightDutyInit

print "waiting for you to press g"
while 1:
    inkey = raw_input()
    if inkey is "g": break

try:
    #forwards(leftDuty,rightDuty,SPEED,455.)
    turn_clockwise(TURN_RATE,90.)
    stop()

except KeyboardInterrupt:
    stop()
