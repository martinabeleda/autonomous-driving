import cv2
import numpy as np
import matplotlib.pyplot as plt

from region_of_interest import region_of_interest
from draw_lines import draw_lines

def lane_detect(img):
    """
    Detects lanes in an image.

    Applies gaussian blur, canny edge detection,
    removes false negatives, hough lines and then
    combines small lines into 2 lanes. Draws the lanes
    on the original image.
    """

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Gaussian Blur
    kernelSize = 5
    blur = cv2.GaussianBlur(gray, (kernelSize,kernelSize), 0)

    # Canny Edge Detection
    lowThreshold = 150
    highThreshold = 200
    edges = cv2.Canny(blur, lowThreshold, highThreshold)

    # Mask out areas outside region of interest
    # Region of interest is defined as a trapezoid to account for perspective
    lowerLeftPoint = [0, 600]
    middleLeftPoint = [0, 450]
    upperLeftPoint = [250, 300]
    upperRightPoint = [550, 300]
    middleRightPoint = [800, 450]
    lowerRightPoint = [800, 600]
    pts = np.array([[lowerLeftPoint, middleLeftPoint, upperLeftPoint,
                   upperRightPoint, middleRightPoint, lowerRightPoint]], dtype=np.int32)
    roi = region_of_interest(edges, pts)

    # Remove false negatives
    kernel = np.ones((5, 5), np.uint8)
    #dilation = cv2.dilate(roi,kernel,iterations = 1)
    closing = cv2.morphologyEx(roi, cv2.MORPH_CLOSE, kernel)

    # Hough Lines
    rho = 1
    theta = np.pi/180
    threshold = 30
    minLineLength = 20
    maxLineGap = 20
    lines = cv2.HoughLinesP(closing, rho, theta, threshold,
                          minLineLength, maxLineGap)

    #masked = cv2.cvtColor(closing, cv2.COLOR_CV_GRAY2RGB)
    masked = closing

    for line in lines:
        for x1,y1,x2,y2 in line:
            cv2.line(masked, (x1, y1), (x2, y2), [0, 0, 255], thickness=2)

    # Display hough lines
    (angle, displacement) = draw_lines(img, lines)

    # Display center line
    cv2.line(img, (400, 0), (400, 600), (255, 0, 0), thickness=2)

    return img, masked, angle, displacement
