#!/bin/bash

DATE=$(date +"%Y-%m-%d_%H%M%S")

raspistill -vf -hf -o /home/pi/camera/$DATE.jpg
scp -i groupc.pem /home/pi/camera/$DATE.jpg ubuntu@54.153.238.139:/var/www/html/exp/
