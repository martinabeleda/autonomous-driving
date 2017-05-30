import RPi.GPIO as GPIO
from motors import *
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

Motor1A = 16
Motor2A = 18

Motor3A = 11
Motor4A = 13

MotorEN = 12

motor_setup()

pwm = GPIO.PWM(MotorEN,100) # 100 Hz frequency
pwm.start(0) # 0% duty cycle

sleep(1)

forwards(50,3)
stop()
GPIO.cleanup()
