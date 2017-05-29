# Lane detection using OpenCV
# Author: Martin Abeleda
# Date: 19/05/2017
import cv2
import numpy as np
import matplotlib.pyplot as plt

from datetime import datetime
from lane_detect import lane_detect

# Read image in color
#img = cv2.imread('images/2017-05-19_120235.jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('images/2017-05-19_120326.jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('images/2017-05-19_120425.jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('images/2017-05-19_120257.jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('images/2017-05-19_120344.jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('images/2017-05-19_120448.jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('images/2017-05-19_120311.jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('images/2017-05-19_120401.jpg', cv2.IMREAD_COLOR)
img = cv2.imread('images/2017-05-19_120511.jpg', cv2.IMREAD_COLOR)
img = cv2.resize(img, (800, 600))

startTime = datetime.now()

# Detect lanes and draw on `img`
(img, angle, topDisplacement, bottomDisplacement) = lane_detect(img)

print datetime.now() - startTime

# Display
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
