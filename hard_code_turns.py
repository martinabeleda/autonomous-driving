from drive import drive_feedback, turn_decide


# def drive_intersection(turnCode)
    # TIME_15CM = 5 # seconds
    # redLineTime = datetime.now()
    # driveTime = datetime.now() - redLineTime
    # while driveTime.total_seconds() < TIME_15CM:
        # driveTime = datetime.now() - redLineTime
	    # drive_feedback()
	
	# if check_light() is GREEN:
	    # turn_decide(turnCode)
	# else:
	    # while check_light() is not GREEN:
		    # stop()
		# turn_decide(turnCode)
		
def forwards(distance)
    SPEED = 100 # mm/s
	time = distance/SPEED
    t1 = datetime.now()
    driveTime = datetime.now() - t1
    while driveTime.total_seconds() < time:
        driveTime = datetime.now() - t1
	    drive_feedback()

def turn_clockwise(angle):
	print "Turn clockwise by", angle, "degrees"
	TURN_RATE = 100
	pi.set_PWM_dutycycle(motorREN,0)
	pi.write(motorL1A, True)
	pi.write(motorL2A, False)
	pi.set_PWM_dutycycle(motorLEN,255)
	time = angle/TURN_RATE
	sleep(time)
	
def turn_anti_clockwise(angle):
	print "Turn anti-clockwise by", angle, "degrees"
	TURN_RATE = 500
	pi.set_PWM_dutycycle(motorLEN,0)
	pi.write(motorR3A, True)
	pi.write(motorR4A, False)
	pi.set_PWM_dutycycle(motorREN,255)
	time = angle/TURN_RATE
	sleep(time)
	
def turn_right():
    print "Turn right"
	forwards(190)
	turn_anti_clockwise(90)

def turn_left():
    print "Turn left"
    forwards(190)
    turn_clockwise(90)