import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

def draw_lines(img, lines, color=[255, 255, 0], thickness=4, horizThresh=0.5, vertThresh=1000):
    """
    This function connects the two `lines` with `color` and `thickness`.
    It ignores `lines` that are close to 0 gradient. It then draws a centre
    line which is the average of the two lines and outputs data regarding the
    centre line so that we can determine the position of the robot within the
    lanes.
    Outputs:
        angle - The angle of the centre line from the vertical. The angle
            indicates the horizontal position of the robot in the lanes. Positive
            angle corresponds to displacement to the right of the lane and vice
            versa.
        topDisplacement - Top displacement indicates the angle that the robot
            is heading. Positive topDisplacement corresponds to the robot pointing
            to the right and vice versa.
        bottomDisplacement - Bottom displacement seems to be affected by both the
            angle and horizontal position of the robot so is not a good indicator
            of either.
    """

    angle = 0
    topDisplacement = 0
    bottomDisplacement = 0

    # These variables represent the y-axis coordinates to which the line will be extrapolated to
    ymin_global = img.shape[0]
    ymax_global = img.shape[0]

    # Right lane line variables
    all_left_grad = []
    all_left_y = []
    all_left_x = []

    # Left lane line variables
    all_right_grad = []
    all_right_y = []
    all_right_x = []

    # Separate hough lines into two opposing lanes, removing cases where lines
    # are nearly horizontal based on thresh. Catch cases where no lines exist.
    try:
        for line in lines:
            for x1,y1,x2,y2 in line:
                gradient, intercept = np.polyfit((x1,x2), (y1,y2), 1)
                ymin_global = min(min(y1, y2), ymin_global)

                if gradient > horizThresh and gradient < vertThresh:
                    all_left_grad += [gradient]
                    all_left_y += [y1, y2]
                    all_left_x += [x1, x2]
                    cv2.line(img, (x1, y1), (x2, y2), [0, 255, 255], thickness=2)

                elif gradient < -horizThresh and gradient > -vertThresh:
                    all_right_grad += [gradient]
                    all_right_y += [y1, y2]
                    all_right_x += [x1, x2]
                    cv2.line(img, (x1, y1), (x2, y2), [255, 0, 255], thickness=2)

        #print 'max left grad = ' + str(max(all_left_grad)) + ' min' + str(min(all_left_grad))
        #print 'max right grad = ' + str(max(all_right_grad)) + ' min' + str(min(all_right_grad))

    except:
        pass

    # Make sure we have some points in each lane line category
    if ((len(all_left_grad) > 0) and (len(all_right_grad) > 0)):



        left_mean_grad = np.mean(all_left_grad)
        left_y_mean = np.mean(all_left_y)
        left_x_mean = np.mean(all_left_x)
        left_intercept = left_y_mean - (left_mean_grad * left_x_mean)

        right_mean_grad = np.mean(all_right_grad)
        right_y_mean = np.mean(all_right_y)
        right_x_mean = np.mean(all_right_x)
        right_intercept = right_y_mean - (right_mean_grad * right_x_mean)

        upper_left_x = int((ymin_global - left_intercept) / left_mean_grad)
        lower_left_x = int((ymax_global - left_intercept) / left_mean_grad)
        upper_right_x = int((ymin_global - right_intercept) / right_mean_grad)
        lower_right_x = int((ymax_global - right_intercept) / right_mean_grad)

        # Draw the lane lines
        cv2.line(img, (upper_left_x, ymin_global), (lower_left_x, ymax_global),
                 color, thickness)
        cv2.line(img, (upper_right_x, ymin_global), (lower_right_x, ymax_global),
                 color, thickness)

        # Draw the centre lane line
        top_x = int(np.mean((upper_left_x, upper_right_x)))
        bottom_x = int(np.mean((lower_left_x, lower_right_x)))

        cv2.line(img, (top_x, ymin_global), (bottom_x, ymax_global),
                 [0, 255, 0], thickness)

        # Calculate angle and displacement of robot in relation to centre line
        angle = math.degrees(math.atan2(top_x - bottom_x, ymax_global - ymin_global))
        topDisplacement = img.shape[1]/2 - top_x
        bottomDisplacement = img.shape[1]/2 - bottom_x

        # Display angle and displacement of robot in relation to centre line
        font = cv2.FONT_HERSHEY_PLAIN
        fontSize = 1
        color = [0, 255, 0]
        cv2.putText(img, 'd_bot = ' + str(bottomDisplacement), (bottom_x + 10, ymax_global - 10),
                    font, fontSize, color)
        cv2.putText(img, 'd_top = ' + str(topDisplacement), (top_x + 10, ymin_global + 10),
                    font, fontSize, color)
        cv2.putText(img, 'alpha = ' + "{0:.2f}".format(angle), (top_x + 10, ymin_global),
                    font, fontSize, color)

    # if we only have the left lane
    elif ((len(all_left_grad) == 0) and (len(all_right_grad) > 0)):

        # draw the right line
        right_mean_grad = np.mean(all_right_grad)
        right_y_mean = np.mean(all_right_y)
        right_x_mean = np.mean(all_right_x)
        right_intercept = right_y_mean - (right_mean_grad * right_x_mean)

        upper_right_x = int((ymin_global - right_intercept) / right_mean_grad)
        lower_right_x = int((ymax_global - right_intercept) / right_mean_grad)

        cv2.line(img, (upper_right_x, ymin_global), (lower_right_x, ymax_global),
                 color, thickness)
        print 'left lane only'
        angle = 0
        topDisplacement = -100
        bottomDisplacement = 0

    # if we only have the right lane
    elif ((len(all_left_grad) > 0) and (len(all_right_grad) == 0)):

        # draw the left line
        left_mean_grad = np.mean(all_left_grad)
        left_y_mean = np.mean(all_left_y)
        left_x_mean = np.mean(all_left_x)
        left_intercept = left_y_mean - (left_mean_grad * left_x_mean)

        upper_left_x = int((ymin_global - left_intercept) / left_mean_grad)
        lower_left_x = int((ymax_global - left_intercept) / left_mean_grad)

        cv2.line(img, (upper_left_x, ymin_global), (lower_left_x, ymax_global),
                 color, thickness)
        print 'right lane only'
        angle = 0
        topDisplacement = 100
        bottomDisplacement = 0

    # No lanes found
    else:

        angle = 0
        topDisplacement = 0
        bottomDisplacement = 0


    return angle, topDisplacement, bottomDisplacement
