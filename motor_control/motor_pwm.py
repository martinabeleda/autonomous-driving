import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

Motor1B = 16
Motor1A = 18
Motor1E = 07

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

pwm = GPIO.PWM(Motor1E,100)
pwm.start(0)

print "Turning motor on"
GPIO.output(Motor1E, True)
GPIO.output(Motor1B, False)
pwm.ChangeDutyCycle(50)
GPIO.output(Motor1A, True)

sleep(2)

GPIO.output(Motor1A, False)

GPIO.output(Motor1B, True)
GPIO.output(Motor1A, False)
pwm.ChangeDutyCycle(75)

sleep(3)

print "Stopping motor"
GPIO.output(Motor1E, False)
pwm.stop()

GPIO.cleanup()
