#!/bin/bash

# xte 'mousemove 900 50' # first method for moving mouse pointer
# xdotool mousemove_relative --polar 180 400 # second method for moving mouse pointer
# sudo xrandr --newmode "800x480_60.00"   29.50  800 824 896 992  480 483 493 500 -hsync +vsync # set new resolution (800x480 60fps)
# sudo xrandr --addmode $MONITOR "800x480_60.00" # set $MONITOR to default display ex. HDMI-1
# sudo xrandr --output $MONITOR --mode "800x480_60.00" # set the new created resolution
# source /home/pi/dashboard/bin/activate # change depends on directory
cd /home/orangepi/dashboardpy_motorcycle_bright/ # change depends on directory
# cat /dev/ttyUSB0 &
# cat /dev/ttyUSB1 &
# cat /dev/ttyUSB2 &
# cat /dev/ttyUSB3 &
python3 main.py # python <= /usr/bin/python3
#python3 main.py # python3 