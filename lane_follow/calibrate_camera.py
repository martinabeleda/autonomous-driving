import numpy
import time
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray

from lane_follow.lane_detect import lane_detect

def calibrate_camera(camera):
    """
    Calibrate shift function
    This function is used to calibrate the angle and top displacement for the
    robot before the program is run. The program asks the user to place the
    robot in the middle of the lane in a variety of places within the map.
    The robot will store the angle and topDisplacement measurements and
    average them to use in order to shift the measurements.
    """
    topDispMeasurements = list()
    angleMeasurements = list()

    # allow the camera to warmup
    time.sleep(1)

    rawCapture = PiRGBArray(camera)

    print "Place the robot in the centre of the lanes and take measurements. Take a number of measurements in a variety of places."

    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        # capture these values when the user hits <p>
        inkey = raw_input("Get measurement. <p> Remove last. <r> Finished? <q>")

        if inkey is "p":
            # take a piccy
            print "Taking measurement"
            # grab an image from the camera
            #camera.capture(rawCapture, format="bgr")
            #image = rawCapture.array

            image = frame.array

            # display the image on screen and wait for a keypress
            cv2.imshow("Image", image)

            # gaussian blur
            kernelSize = 5
            blur = cv2.GaussianBlur(image, (kernelSize,kernelSize), 0)

            # detect lanes in the image
            (img, angle, topDisp, bottomDisp) = lane_detect(blur)

            topDispMeasurements.append(topDisp)
            angleMeasurements.append(angle)

        elif inkey is "r" and len(topDispMeasurements) > 0 and len(angleMeasurements) > 0:

            #remove element from list
            print "Remove last element from list"
            del topDispMeasurements[-1]
            del angleMeasurements[-1]

        elif inkey is "q":

            print "Done"
            break

        rawCapture.truncate(0)

    topDispMean = numpy.mean(topDispMeasurements)
    angleMean = numpy.mean(angleMeasurements)

    return topDispMean, angleMean
