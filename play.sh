#!/bin/bash
ISRUNNING=$(ps ax |grep -v grep |grep -c "omxplayer")
CURRENTFOLDER=$(cat /home/pi/fld.tmp)
CURRENTFILE=($CURRENTFOLDER/*)
printf "%s\n" "${CURRENTFILE[RANDOM % ${#CURRENTFILE[@]}]}" > hang.txt
HANG=$(cat hang.txt)
echo "Now playing:" $HANG

if [ $ISRUNNING -eq 0 ]; then
	omxplayer /home/pi/media/others/felvesz.wav
	omxplayer $HANG
	omxplayer /home/pi/media/others/letesz.wav
		else
	echo "omxplayer is running, exiting!"
	exit;
fi
