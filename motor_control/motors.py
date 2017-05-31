#import RPi.GPIO as GPIO
from time import sleep
import pigpio

pi = pigpio.pi()

#GPIO.setmode(GPIO.BOARD)

#Motor1A = 16
#Motor2A = 18

Motor1A = 23
Motor2A = 24

#Motor3A = 11
#Motor4A = 13

Motor3A = 17
Motor4A = 27

#MotorEN = 12

Motor12EN = 18
Motor34EN = 22

#GPIO.setup(MotorEN, GPIO.OUT)
#pwm = GPIO.PWM(MotorEN,100) # 100 Hz frequency

def motor_setup():
	print "Setup Motor GPIO"
	pi.set_mode(Motor1A, pigpio.OUTPUT)
	pi.set_mode(Motor2A, pigpio.OUTPUT)
	pi.set_mode(Motor3A, pigpio.OUTPUT)
	pi.set_mode(Motor4A, pigpio.OUTPUT)
	pi.set_mode(Motor12EN, pigpio.OUTPUT)
	pi.set_mode(Motor34EN, pigpio.OUTPUT)
	pi.set_PWM_frequency(Motor12EN, 100) # 100 Hz frequency
	pi.set_PWM_frequency(Motor34EN, 100)
#	GPIO.setup(Motor1A, GPIO.OUT)
#	GPIO.setup(Motor2A, GPIO.OUT)
#	GPIO.setup(Motor3A, GPIO.OUT)
#	GPIO.setup(Motor4A, GPIO.OUT)
#	GPIO.setup(MotorEN, GPIO.OUT)

def forwards(dc,distance):
	print "Forwards"
	SPEED = 39 # mm/s
#	GPIO.output(Motor1A, GPIO.HIGH)
#	GPIO.output(Motor2A, GPIO.LOW)
#	GPIO.output(Motor3A, GPIO.HIGH)
#	GPIO.output(Motor4A, GPIO.LOW)
	pi.write(Motor1A, True)
	pi.write(Motor2A, False)
	pi.write(Motor3A, True)
	pi.write(Motor4A, False)

#	pwm.ChangeDutyCycle(dc)
	pi.set_PWM_dutycycle(Motor12EN,dc)
	dcR = dc-dc/2.8
	pi.set_PWM_dutycycle(Motor34EN,dcR)
	print dcR
	time = distance/SPEED

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
	#pwm.stop()
	pi.set_PWM_dutycycle(Motor12EN, 0)
	pi.set_PWM_dutycycle(Motor34EN, 0)
