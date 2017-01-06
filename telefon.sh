#!/bin/bash
# Original file is /home/pi/bin/telefon.sh
source /etc/profile

# Parameters of telefon.py
# Receiver switch phisical GPIO no.
# Folderselector switch phisical GPIO no.
# Receiver switch reverser 0 or 1
# Script to run when receiver is up
# Script to run when receiver is down
# Temporary file for folder selection
# if exist "d" is for debug mode - not mandatory

sudo python /usr/bin/telefon.py 7 19 0 felvesz.sh letesz.sh /home/pi/fld.tmp d &

# Turn on led when telefon.py is ready
# gpio parameters
# mode # LED phisical no., in or out
# write # LED phisical no., 1 when on, 0 when off

gpio mode 29 out
gpio write 29 1
