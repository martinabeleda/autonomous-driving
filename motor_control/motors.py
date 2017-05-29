import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor2A = 18
Motor12EN = 22

Motor3A = 11
Motor4A = 13
Motor34EN = 15

def motor_setup(self)
	print "Setup Motor GPIO"
	GPIO.setup(Motor1A, GPIO.OUT)
	GPIO.setup(Motor2A, GPIO.OUT)
	GPIO.setup(Motor12EN, GPIO.OUT)
	GPIO.setup(Motor3A, GPIO.OUT)
	GPIO.setup(Motor4A, GPIO.OUT)
	GPIO.setup(Motor34EN, GPIO.OUT)

def forwards(self, distance)
	speed = 1
	print "Forwards"
	GPIO.output(Motor1A, GPIO.HIGH)
	GPIO.output(Motor2A, GPIO.LOW)
	GPIO.output(Motor3A, GPIO.HIGH)
	GPIO.output(Motor4A, GPIO.LOW)
	GPIO.output(Motor12EN, GPIO.HIGH)
	GPIO.output(Motor34EN, GPIO.HIGH)
	time = distance / speed
	sleep(time)

def reverse(self, distance)
	print "Reverse"
	GPIO.output(Motor1A, GPIO.LOW)
	GPIO.output(Motor2A, GPIO.HIGH)
	GPIO.output(Motor3A, GPIO.LOW)
	GPIO.output(Motor4A, GPIO.HIGH)
	GPIO.output(Motor12EN, GPIO.HIGH)
	GPIO.output(Motor34EN, GPIO.HIGH)
	time = distance / speed
	sleep(time)

def turn_clockwise(self, angle)
	print "Turn clockwise by", angle, "degrees"
	GPIO.output(Motor1A, GPIO.HIGH)
	GPIO.output(Motor2A, GPIO.LOW)
	GPIO.output(Motor3A, GPIO.LOW)
	GPIO.output(Motor4A, GPIO.HIGH)
	GPIO.output(Motor12EN, GPIO.HIGH)
	GPIO.output(Motor34EN, GPIO.HIGH)
	time = angle/turnRate
	sleep(time)

def return_to_centre(self,angle,distance)
	if angle > 0
		turnAntiClockWise(angle)
	else
		turnClockwise(abs(angle))

	forwards(distance)

def left_turn(self)
	self.forwards(1)
	self.turnAntiClockWise(90)
	self.forwards(1)

def right_turn(self)
	self.forwards(1)
	self.turnClockwise(90)
	self.forwards(1)

def turn_anti_clockwise(self, angle)
	print "Turn anti-clockwise by", angle, "degrees"
	GPIO.output(Motor1A, GPIO.LOW)
	GPIO.output(Motor2A, GPIO.HIGH)
	GPIO.output(Motor3A, GPIO.HIGH)
	GPIO.output(Motor4A, GPIO.LOW)
	GPIO.output(Motor12EN, GPIO.HIGH)
	GPIO.output(Motor34EN, GPIO.HIGH)
	time = angle/turnRate
	sleep(time)

def stop(self)
	print "Stop"
	GPIO.output(Motor12EN, GPIO.LOW)
	GPIO.output(Motor34EN, GPIO.LOW)
