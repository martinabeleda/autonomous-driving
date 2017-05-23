import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

def draw_lines(img, lines, color=[255, 255, 0], thickness=4, thresh=0.15):
    """
    This function connects the two `lines` with `color` and `thickness`.
    It ignores `lines` that are close to 0 gradient.
    """

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

        # Calculate the position and angle of the robot in relation to the lanes
        top_x = int(np.mean((upper_left_x, upper_right_x)))
        bottom_x = int(np.mean((lower_left_x, lower_right_x)))

        cv2.line(img, (top_x, ymin_global), (bottom_x, ymax_global), [0, 255, 0], thickness)

    # Only one line has been detected
    #else
        # Call curve following algorithm

    # Calculate angle and displacement of robot in relation to centre line
    angle = math.degrees(math.atan((top_x - bottom_x)/(ymax_global - ymin_global)))
    displacement = bottom_x - img.shape[1]/2

    return angle, displacement
