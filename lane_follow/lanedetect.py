# Lane detection using OpenCV
# Author: Martin Abeleda
# Date: 19/05/2017
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read image in grayscale
#IMREAD_GRAYSCALE
#IMREAD_COLOR
#IMREAD_UNCHANGED
img = cv2.imread('images/2017-05-19_120235.jpg', cv2.IMREAD_GRAYSCALE)

# Extract ROI
roi = img[0:2592, 972:1944]

# Show image using cv
# cv2.imshow('image', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# Plot image using matplotlib
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
plt.plot([1296, 1296], [0, 1944], 'c', linewidth = 1.5)
plt.axis([0, 2592, 1944, 972])
plt.show()
