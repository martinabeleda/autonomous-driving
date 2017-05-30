import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor2A = 18
Motor12EN = 12

Motor3A = 11
Motor4A = 13
Motor34EN = 33

def motor_setup():
	print "Setup Motor GPIO"
	GPIO.setup(Motor1A, GPIO.OUT)
	GPIO.setup(Motor2A, GPIO.OUT)
	GPIO.setup(Motor12EN, GPIO.OUT)
	GPIO.setup(Motor3A, GPIO.OUT)
	GPIO.setup(Motor4A, GPIO.OUT)
	GPIO.setup(Motor34EN, GPIO.OUT)

def forwards(pwm1,pwm2,duty,time):
	print "Forwards"
	GPIO.output(Motor1A, GPIO.HIGH)
	GPIO.output(Motor2A, GPIO.LOW)
	pwm1.ChangeDutyCycle(duty)
	GPIO.output(Motor3A, GPIO.HIGH)
	GPIO.output(Motor4A, GPIO.LOW)
	pwm2.ChangeDutyCycle(duty)
	sleep(time)

def reverse(pwm1,pwm2,distance):
	print "Reverse"
	GPIO.output(Motor1A, GPIO.LOW)
	GPIO.output(Motor2A, GPIO.HIGH)
	pwm1.ChangeDutyCycle(duty)
	GPIO.output(Motor3A, GPIO.LOW)
	GPIO.output(Motor4A, GPIO.HIGH)
	pwm2.ChangeDutyCycle(duty)
	sleep(time)

def turn_clockwise(pwm1,pwm2,angle):
	print "Turn clockwise by", angle, "degrees"
	turnRate = 100
	GPIO.output(Motor1A, GPIO.HIGH)
	GPIO.output(Motor2A, GPIO.LOW)
	pwm1.ChangeDutyCycle(100)
	GPIO.output(Motor3A, GPIO.LOW)
	GPIO.output(Motor4A, GPIO.HIGH)
	pwm2.ChangeDutyCycle(100)
	time = angle/turnRate
	sleep(time)
	
def turn_anti_clockwise(pwm1,pwm2,angle):
	print "Turn anti-clockwise by", angle, "degrees"
	turnRate = 100
	GPIO.output(Motor1A, GPIO.LOW)
	GPIO.output(Motor2A, GPIO.HIGH)
	pwm1.ChangeDutyCycle(100)
	GPIO.output(Motor3A, GPIO.HIGH)
	GPIO.output(Motor4A, GPIO.LOW)
	pwm2.ChangeDutyCycle(100)
	time = angle/turnRate
	sleep(time)

def return_to_centre(angle,distance):
	if angle > 0:
		turnAntiClockWise(angle)
	else:
		turnClockwise(abs(angle))

	forwards(50,distance)

def left_turn():
	self.forwards(50,1)
	self.turnAntiClockWise(90)
	self.forwards(50,1)

def right_turn():
	self.forwards(1)
	self.turnClockwise(90)
	self.forwards(1)

def stop(pwm1,pwm2):
	print "Stop"
	pwm1.stop()
	pwm2.stop()
