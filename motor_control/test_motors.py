import RPi.GPIO as GPIO
from motors import *
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

Motor1A = 16
Motor2A = 18
Motor12EN = 22

Motor3A = 11
Motor4A = 13
Motor34EN = 15

motor_setup()

pwm1 = GPIO.PWM(Motor12EN,100) # 100 Hz frequency
pwm1.start(0) # 0% duty cycle
pwm2 = GPIO.PWM(Motor34EN,100)
pwm2.start(0)

sleep(1)

forwards(50,3)
stop()

