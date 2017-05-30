import RPi.GPIO as GPIO
from motors import *
from time import sleep

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

Motor1A = 16
Motor2A = 18
Motor12EN = 12

Motor3A = 11
Motor4A = 13
Motor34EN = 33

motor_setup()

pwm1 = GPIO.PWM(Motor12EN,50) # 100 Hz frequency
pwm1.start(0) # 0% duty cycle
pwm2 = GPIO.PWM(Motor34EN,50)
pwm2.start(0)

sleep(1)

forwards(pwm1,pwm2,80,3)
stop(pwm1,pwm2)
GPIO.cleanup()
