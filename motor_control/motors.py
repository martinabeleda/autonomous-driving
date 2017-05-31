#import RPi.GPIO as GPIO
#import os
#cmd = 'sudo pigpiod'
#os.system(cmd)
from time import sleep
import pigpio

pi = pigpio.pi()

#GPIO.setmode(GPIO.BOARD)

#MotorL1A = 16
#MotorL2A = 18

MotorL1A = 23
MotorL2A = 24

#MotorR3A = 11
#MotorR4A = 13

MotorR3A = 17
MotorR4A = 27

#MotorEN = 12

MotorLEN = 18
MotorREN = 22

#GPIO.setup(MotorEN, GPIO.OUT)
#pwm = GPIO.PWM(MotorEN,100) # 100 Hz frequency

def motor_setup():
	print "Setup Motor GPIO"
	pi.set_mode(MotorL1A, pigpio.OUTPUT)
	pi.set_mode(MotorL2A, pigpio.OUTPUT)
	pi.set_mode(MotorR3A, pigpio.OUTPUT)
	pi.set_mode(MotorR4A, pigpio.OUTPUT)
	pi.set_mode(MotorLEN, pigpio.OUTPUT)
	pi.set_mode(MotorREN, pigpio.OUTPUT)
	pi.set_PWM_frequency(MotorLEN, 100) # 100 Hz frequency
	pi.set_PWM_frequency(MotorREN, 100)
#	GPIO.setup(MotorL1A, GPIO.OUT)
#	GPIO.setup(MotorL2A, GPIO.OUT)
#	GPIO.setup(MotorR3A, GPIO.OUT)
#	GPIO.setup(MotorR4A, GPIO.OUT)
#	GPIO.setup(MotorEN, GPIO.OUT)

def forwards(dc,distance):
	print "Forwards"
	SPEED = 39 # mm/s
#	GPIO.output(MotorL1A, GPIO.HIGH)
#	GPIO.output(MotorL2A, GPIO.LOW)
#	GPIO.output(MotorR3A, GPIO.HIGH)
#	GPIO.output(MotorR4A, GPIO.LOW)
	pi.write(MotorL1A, True)
	pi.write(MotorL2A, False)
	pi.write(MotorR3A, True)
	pi.write(MotorR4A, False)

#	pwm.ChangeDutyCycle(dc)
	pi.set_PWM_dutycycle(MotorLEN,dc)
	dcR = dc-dc/2.8
	pi.set_PWM_dutycycle(MotorREN,dcR)
	print dcR
	time = distance/SPEED
	sleep(time)

def reverse(distance):
	print "Reverse"
	SPEED = 39 # mm/s
	pi.write(MotorL1A, False)
	pi.write(MotorL2A, True)
	pi.write(MotorR3A, False)
	pi.write(MotorR4A, True)
	pi.set_PWM_dutycycle(MotorLEN,dc)
	dcR = dc-dc/2.6
	pi.set_PWM_dutycycle(MotorREN,dcR)
	print dcR
	time = distance/SPEED
	sleep(time)

def turn_clockwise(angle):
	print "Turn clockwise by", angle, "degrees"
	TURN_RATE = 100
	pi.set_PWM_dutycycle(MotorREN,0)
	pi.write(MotorL1A, True)
	pi.write(MotorL2A, False)
	pi.set_PWM_dutycycle(MotorLEN,255)
	time = angle/TURN_RATE
	sleep(time)
	
def turn_anti_clockwise(angle):
	print "Turn anti-clockwise by", angle, "degrees"
	TURN_RATE = 100
	pi.set_PWM_dutycycle(MotorLEN,0)
	pi.write(MotorR3A, True)
	pi.write(MotorR4A, False)
	pi.set_PWM_dutycycle(MotorREN,255)
	time = angle/TURN_RATE
	sleep(time)

# def return_to_centre(angle,distance):
	# if angle > 0:
		# turnAntiClockWise(angle)
	# else:
		# turnClockwise(abs(angle))

	# self.forwards(50,distance)

def left_turn():
	"Left turn"
	self.forwards(160,225)
	self.turnAntiClockWise(90)
	self.forwards(160,140)

def right_turn():
	"Left turn"
	self.forwards(160,225)
	self.turnClockwise(90)
	self.forwards(160,140)

def stop():
	print "Stop"
	#pwm.stop()
	pi.set_PWM_dutycycle(MotorLEN, 0)
	pi.set_PWM_dutycycle(MotorREN, 0)
