import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

motor1A = 11
motor1B = 13
motor1E = 15
motor2A = 16
motor2B = 18
motor2E = 22

GPIO.setup(motor1A, GPIO.OUT)
GPIO.setup(motor1B, GPIO.OUT)
GPIO.setup(motor1E, GPIO.OUT)
GPIO.setup(motor2A, GPIO.OUT)
GPIO.setup(motor2B, GPIO.OUT)
GPIO.setup(motor2E, GPIO.OUT)

var = 1
while var == 1:


GPIO.cleanup()