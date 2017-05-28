# PiCar
Lane following and traffic sign reading differential drive robot. Developed for MTRX5700 Experimental Robotics Major Project 2017 by:

* Martin Abeleda
* Tom Rapson
* Kristina Mahoney
* Riley Green

## Dependencies

* Raspberry Pi 3 with raspbian
  * Picamera
  * L293D H-bridge
  * Adafruit Mini Robot Rover Chassis Kit
* Open CV
* Python 2.7

## Cloning

```
git clone https://github.com/martinabeleda/PiCar.git
```

## PiCar setup

The Pi is configured to startup in Command Line Interface (CLI) mode and automatically logged in as pi. This saves memory and startup time because the front end GUI doesn't have to load. To manually start the desktop GUI, type `startx` into CLI.

The password for the default user has been set to `picar`.

First, I set up hotspot on my phone and connect both the Pi and my laptop to it. Note that the IP address may change when the Pi is connected to different wifi. SSH instructions:

Marty's pi:

```
pi@raspberrypi:~ $ ssh pi@192.168.43.94
pi@192.168.43.94's password: picar
```

Tom's Pi:
```
pi@raspberrypi:~ $ ssh pi@192.168.43.118
pi@192.168.43.118's password: picar
```

Click [here](http://mitchtech.net/raspberry-pi-opencv/) for instructions to install OpenCV on the Pi. 

## Remote Desktop

Click [here](https://www.element14.com/community/docs/DOC-78170/l/connecting-to-a-remote-desktop-on-the-raspberry-pi) to see instructions for connecting the Pi to remote desktop on your computer.  

Remote desktop software for your computer:   

  Linux: `sudo apt-get install rdesktop`  
  Mac: search "remote desktop" in App store  
  
For linux, run `rdesktop -g 90% 192.168.43.94` or`rdesktop -g 90% 192.168.43.118` in terminal.  
  
Login with the following credentials:  

```
Module: sesman-Xvnc
username: pi
password: picar
```
 
