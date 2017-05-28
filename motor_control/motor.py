import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

Motor1A = 16
Motor2A = 18
Motor12EN = 22

Motor3A = 11
Motor4A = 13
Motor34EN = 15

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor12EN, GPIO.OUT)
GPIO.setup(Motor3A, GPIO.OUT)
GPIO.setup(Motor4A, GPIO.OUT)
GPIO.setup(Motor34EN, GPIO.OUT)

print "Turning motor on"
GPIO.output(Motor1A, GPIO.HIGH)
GPIO.output(Motor2A, GPIO.LOW)
GPIO.output(Motor3A, GPIO.HIGH)
GPIO.output(Motor4A, GPIO.LOW)
GPIO.output(Motor12EN, GPIO.HIGH)
GPIO.output(Motor34EN, GPIO.HIGH)

sleep(3)

print "Reverse"
GPIO.output(Motor1A, GPIO.LOW)
GPIO.output(Motor2A, GPIO.HIGH)
GPIO.output(Motor3A, GPIO.LOW)
GPIO.output(Motor4A, GPIO.HIGH)
GPIO.output(Motor12EN, GPIO.HIGH)
GPIO.output(Motor34EN, GPIO.HIGH)

sleep(3)

print "Stopping motor"
GPIO.output(Motor12EN, GPIO.LOW)
GPIO.output(Motor34EN, GPIO.LOW)

GPIO.cleanup()
