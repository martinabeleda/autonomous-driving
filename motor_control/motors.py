import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor2A = 18

Motor3A = 11
Motor4A = 13

MotorEN = 12

GPIO.setup(MotorEN, GPIO.OUT)
pwm = GPIO.PWM(MotorEN,100) # 100 Hz frequency

def motor_setup():
	print "Setup Motor GPIO"
	GPIO.setup(Motor1A, GPIO.OUT)
	GPIO.setup(Motor2A, GPIO.OUT)
	GPIO.setup(Motor3A, GPIO.OUT)
	GPIO.setup(Motor4A, GPIO.OUT)

def forwards(duty,time):
	print "Forwards"
	pwm.ChangeDutyCycle(duty)
	GPIO.output(Motor1A, GPIO.HIGH)
	GPIO.output(Motor2A, GPIO.LOW)
	GPIO.output(Motor3A, GPIO.HIGH)
	GPIO.output(Motor4A, GPIO.LOW)
	sleep(time)

def reverse(distance):
	print "Reverse"
	pwm.ChangeDutyCycle(duty)
	GPIO.output(Motor1A, GPIO.LOW)
	GPIO.output(Motor2A, GPIO.HIGH)
	GPIO.output(Motor3A, GPIO.LOW)
	GPIO.output(Motor4A, GPIO.HIGH)
	sleep(time)

def turn_clockwise(angle):
	print "Turn clockwise by", angle, "degrees"
	turnRate = 100
	GPIO.output(Motor1A, GPIO.HIGH)
	GPIO.output(Motor2A, GPIO.LOW)
	GPIO.output(Motor3A, GPIO.LOW)
	GPIO.output(Motor4A, GPIO.HIGH)
	pwm.ChangeDutyCycle(100)
	time = angle/turnRate
	sleep(time)
	
def turn_anti_clockwise(angle):
	print "Turn anti-clockwise by", angle, "degrees"
	turnRate = 100
	GPIO.output(Motor1A, GPIO.LOW)
	GPIO.output(Motor2A, GPIO.HIGH)
	GPIO.output(Motor3A, GPIO.HIGH)
	GPIO.output(Motor4A, GPIO.LOW)
	pwm.ChangeDutyCycle(100)
	time = angle/turnRate
	sleep(time)

def return_to_centre(angle,distance):
	if angle > 0:
		turnAntiClockWise(angle)
	else:
		turnClockwise(abs(angle))

	self.forwards(50,distance)

def left_turn():
	self.forwards(50,1)
	self.turnAntiClockWise(90)
	self.forwards(50,1)

def right_turn():
	self.forwards(1)
	self.turnClockwise(90)
	self.forwards(1)

def stop():
	print "Stop"
	pwm.stop()
