import RPi.GPIO as GPIO
import time
import sys
import subprocess

# test
counter = 0

prev_fld = 0

#list of folders to use
folders = ["/home/pi/media/vers", "/home/pi/media/mese"]
#folder to use
folderToUse = ""

if (len(sys.argv)<7):
	print("Usage: [GPIO.KAGYLO] [GPIO.MAPPASZELEKTOR] [IRANYVALTO] [SZKRIPT1] [SZKRIPT2] [LEJATSZANDO_MAPPA] <DEBUG_MOD>")
	exit(-1)

#if we have a 7th argument and it is a 'd' we will print out debug information to the console
if (len(sys.argv)>=8):
	if(sys.argv[7]=='d'):
		dbg = True
else:
	dbg = False

#if 1 the playback starts when the GPIO port phoneSwitch is 1
switchMode = int(sys.argv[3])

def printDebug(typ):
	if dbg==False:
		return 0
	if(typ=='DISPLAY_PHONESWITCH_LEVEL'):
		print("phone switch level: "+str(GPIO.input(phoneSwitch))+"("+str(GPIO.input(phoneSwitch)==switchMode)+")")
	if(typ=='DISPLAY_FOLDERSWITCH_LEVEL'):
		print("folder switch level: "+str(prev_fld)+"::")
	if(typ=='DISPLAY_WHAT_TO_PLAY'):
		print("start playback: "+folders[GPIO.input(folderSwitch)])
	if(typ=='DISPLAY_CALL_END'):
		print("KUTYA")
	if(typ=='DISPLAY_BUTTON_PRESS_COUNTER'):
		print ''
		#global counter
	        #print("megnyomva: "+str(counter))
	        #counter += 1
	if(typ=='DISPLAY_SELECTED_FOLDER'):
		global counter
		print("Folder selected: "+str(counter)+" "+folders[GPIO.input(folderSwitch)])
		counter += 1

def managePlayback(channel):
	printDebug('DISPLAY_PHONESWITCH_LEVEL')
	#if GPIO level = switchMode => start playback (kagylo felemelve)
	if (GPIO.input(phoneSwitch)==switchMode):
		printDebug('DISPLAY_WHAT_TO_PLAY')
		subprocess.call([sys.argv[4]])
	else:
		printDebug('DISPLAY_CALL_END')
		subprocess.call([sys.argv[5]])

def selectFolder(channel):
	global prev_fld

	fld = GPIO.input(folderSwitch)

	prev_fld = fld

	#if((not prev_fld) and (fld)):
	printDebug('DISPLAY_FOLDERSWITCH_LEVEL')
	GPIO.output(23,fld)
	# file descriptor; this file will contain the current folder path
	f = open(sys.argv[6], 'w')
	f.write(folders[fld]+"\n")
	f.close()

#phone switch
phoneSwitch = int(sys.argv[1])
#folder selection switch (verse or tale)
folderSwitch = int(sys.argv[2])

GPIO.setmode(GPIO.BOARD)

GPIO.setup(phoneSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(folderSwitch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(23, GPIO.OUT)

GPIO.add_event_detect(phoneSwitch, GPIO.BOTH, callback=managePlayback, bouncetime=300)
GPIO.add_event_detect(folderSwitch, GPIO.BOTH, callback=selectFolder)

try:
	while True:
		time.sleep(1)
finally:
	GPIO.cleanup()
