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

sleep(1)

forwards(50,3)
stop()
