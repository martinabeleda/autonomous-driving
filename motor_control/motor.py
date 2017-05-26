import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor1B = 18
Motor1E = 22

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

print "Turning motor on"
GPIO.output(Motor1E, GPIO.HIGH)

for i in range(0,1000):
	GPIO.output(Motor1A, i%2)
	GPIO.output(Motor1B, not(i%2))
	sleep(0.1)
	print i
	
sleep(2)

print "Stopping motor"
GPIO.output(Motor1E, GPIO.LOW)

GPIO.cleanup()
