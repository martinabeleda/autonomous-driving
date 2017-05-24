# PiCar
Experimental robotics major project - multi-robot autonomous car network

## Cloning

```
git clone https://github.com/martinabeleda/PiCar.git
```

## PiCar setup

The Pi is configured to startup in Command Line Interface (CLI) mode and automatically logged in as pi. This saves memory and startup time because the front end GUI doesn't have to load. To manually start the desktop GUI, type `startx` into CLI.

The password for the default user has been set to `picar`.

First, I set up hotspot on my phone and connect both the Pi and my laptop to it. 

To ssh into the pi:

```
pi@raspberrypi:~ $ ssh pi@192.168.43.94
pi@192.168.43.94's password: picar
```

Click [here](http://mitchtech.net/raspberry-pi-opencv/) for instructions to install OpenCV on the Pi. 

## Remote Desktop

Click [here](https://www.element14.com/community/docs/DOC-78170/l/connecting-to-a-remote-desktop-on-the-raspberry-pi) to see instructions for connecting the Pi to remote destop on your computer.

To install remote desktop software on the Pi:
```
sudo apt-get install xrdp
```
Remote desktop software for your computer:

  Linux: `sudo apt-get install rdesktop`
  Mac: search "remote destop" in App store
  
For linux, run `rdesktop 192.168.43.94` in terminal.
  
Login with the following credentials:

```
Module: sesman-Xvnc
username: pi
password: picar
```
  
  
