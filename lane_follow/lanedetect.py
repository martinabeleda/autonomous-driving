# Lane detection using OpenCV
# Author: Martin Abeleda
# Date: 19/05/2017
import cv2
import numpy as np
import matplotlib.pyplot as plt

"""
Applies an image mask.

Only keeps the region of the image defined by the polygon
formed from `vertices`. The rest of the image is set to black.
"""
def region_of_interest(img, vertices):

    #defining a blank mask to start with
    mask = np.zeros_like(img)

    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

"""
This function draws `lines` with `color` and `thickness`.
"""
def draw_lines(img, lines, color=[255, 255, 0], thickness=4, thresh=0.15):

    imshape = img.shape

    # these variables represent the y-axis coordinates to which the line will be extrapolated to
    ymin_global = img.shape[0]
    ymax_global = img.shape[0]

    # left lane line variables
    all_left_grad = []
    all_left_y = []
    all_left_x = []

    # right lane line variables
    all_right_grad = []
    all_right_y = []
    all_right_x = []

    for line in lines:
        for x1,y1,x2,y2 in line:
            gradient, intercept = np.polyfit((x1,x2), (y1,y2), 1)
            ymin_global = min(min(y1, y2), ymin_global)

            if (gradient > 0 + thresh):
                all_left_grad += [gradient]
                all_left_y += [y1, y2]
                all_left_x += [x1, x2]
            elif (gradient < 0 - thresh):
                all_right_grad += [gradient]
                all_right_y += [y1, y2]
                all_right_x += [x1, x2]

    left_mean_grad = np.mean(all_left_grad)
    left_y_mean = np.mean(all_left_y)
    left_x_mean = np.mean(all_left_x)
    left_intercept = left_y_mean - (left_mean_grad * left_x_mean)

    right_mean_grad = np.mean(all_right_grad)
    right_y_mean = np.mean(all_right_y)
    right_x_mean = np.mean(all_right_x)
    right_intercept = right_y_mean - (right_mean_grad * right_x_mean)

    # Make sure we have some points in each lane line category
    if ((len(all_left_grad) > 0) and (len(all_right_grad) > 0)):
        upper_left_x = int((ymin_global - left_intercept) / left_mean_grad)
        lower_left_x = int((ymax_global - left_intercept) / left_mean_grad)
        upper_right_x = int((ymin_global - right_intercept) / right_mean_grad)
        lower_right_x = int((ymax_global - right_intercept) / right_mean_grad)

        cv2.line(img, (upper_left_x, ymin_global), (lower_left_x, ymax_global), color, thickness)
        cv2.line(img, (upper_right_x, ymin_global), (lower_right_x, ymax_global), color, thickness)

# Read image in color
#IMREAD_GRAYSCALE
#IMREAD_COLOR
#IMREAD_UNCHANGED
img = cv2.imread('images/2017-05-19_120235.jpg', cv2.IMREAD_COLOR)
#img = cv2.imread('images/2017-05-19_120425.jpg', cv2.IMREAD_COLOR)

# Resize and convert to grayscale
img = cv2.resize(img, (800, 600))
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

print(lines)

# Display hough lines
draw_lines(img, lines)

# Display center line
cv2.line(img, (400, 0), (400, 600), (255, 0, 0), thickness=2)

# Display
cv2.imshow('image', img)
cv2.imshow('canny', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
