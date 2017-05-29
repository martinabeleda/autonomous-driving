# Lane Following Module

Credit to [Vijay Ramakrishnan](https://github.com/vijay120/Autonomous-Vehicles)

The lane following module implements lane detection using the Python OpenCV API. This module also sends motor control commands based on the position of the robot within the lanes.

`lane_follow.py` contains OpenCV code for lane detection using Python2.7 on a PC.

`pi_lane_follow.py` is the implementation for Raspberry Pi 3 using the `picamera` module.

Test images are contained within the `\images` directory.

## Usage

Lane detection is implemented in the `lane_detect()` function which takes in an image from the picamera in the resolution 800x600. The module processes the image and outputs the following:

1. `img` - The original image with lanes (cyan), centre line (green) and robot position (blue) overlayed;
2. `masked` - The image of the masked area with the hough lines (red) overlayed;
3. `angle` - The angle between the robot heading and the centre line of the lanes;
4. `displacement` - The displacement between the bottom of the lane centre line and the robot heading line.

Examples of the output image are below:

![](https://github.com/martinabeleda/PiCar/blob/master/lane_follow/images/lane_follow1.png)

## Processing
The image processing is:
1. Convert to grayscale;
2. Remove noise using Gaussian blur;
3. Canny Edge detection;
4. Extract region of interest;
5. Remove false negatives (closing);
6. Hough lines; and
7. Aggregate hough lines into 2 lanes. 

## Links
### Lane Following
[OpenCV car lanes](https://medium.com/@vijay120/detecting-car-lane-lines-using-computer-vision-d23b2dafdf4c)  
[Curved and straight lanes](https://drive.google.com/file/d/0B3rXba6M6OXhdlJMNVEtenhTNHc/view)  

### Open CV
[Feature Detection Documentation](http://docs.opencv.org/2.4/modules/imgproc/doc/feature_detection.html?highlight=canny)   
[Open CV Video on Pi](http://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/)
