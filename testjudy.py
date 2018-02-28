import judy
import datetime
import subprocess
import time
import cv2
import fileinput
import pygame
import RPi.GPIO as GPIO
import sys
import os

global running
running = True

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def restart_program():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)

#def killJudy():
#    global running
#    kill = "sudo killall pocketsphinx_continuous"
#    subprocess.Popen(kill, shell=True)
#    judy.__del__()
#    judy.listen(None, None, None, callsign=None, attention_span=0, forever=False, running=False)
    #running = False
    #print running
#    kill = "sudo killall pocketsphinx_continuous"
#    subprocess.Popen(kill, shell=True)

#def startJudy():
#    judy.listen(vin, vout, handle, callsign='Pi', attention_span=10, forever=True, running=True)


#def toggleVoiceCommands(channel):
#    kill = "sudo killall pocketsphinx_continuous"
#    subprocess.Popen(kill, shell=True)
#    global running
#    print "button pushed"
#    print running
#    if running == True:
	#running = False
#	print running
#	killJudy()
#        kill = "sudo killall pocketsphinx_continuous"
#        subprocess.Popen(kill, shell=True)
#        judy.__del__()
#	judy.listen(None, None, None, callsign='Pi', attention_span=10, forever=True, running=False)
	#judy.listen(None, None, None, callsign='Pi', attention_span=0, forever=False, running=False)
	#judy.__del__()
	
#	running = False
#	print running
#    elif running == False:
#	print running
	#judy.listen(vin, vout, handle, callsign='Pi', attention_span=10, forever=True, running=True)
#	startJudy()
#	running = True
	#restart_program()
    #global running
    #if running == True:
    #    running = False
    #else:
    #    running = True


#GPIO.add_event_detect(19, GPIO.FALLING, callback=toggleVoiceCommands, bouncetime=300)

vin = judy.VoiceIn(adcdev='plughw:1,0',
                   lm='/home/pi/judy/1918.lm',
                   dict='/home/pi/judy/1918.dic')

vout = judy.VoiceOut(device='plughw:0,0',
                     resources='/home/pi/judy/resources/audio')

def get_file_name_pic():  # new
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")

def get_file_name_vid():  # new
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")

def line_prepender(filename, line):
    with open(filename, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(line.rstrip('\r\n') + '\n' + content)

def handle(phrase):
    print 'Heard:', phrase
    #vout.say(phrase)
    if "TAKE" in phrase.upper() and "PICTURE" in phrase.upper():
        filename = get_file_name_pic()
        photo = "raspistill -o /home/pi/"+filename+" -rot 270"
        subprocess.Popen(photo, shell=True)
        vout.say("Taking Picture")
        photofile = "/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/"+filename+" /Apps/PiGlass/"+filename
        line_prepender("picfiles.txt", filename)
        time.sleep(7)
        subprocess.Popen(photofile, shell=True)

    if "TAKE" in phrase.upper() and "VIDEO" in phrase.upper():
        videoFile = get_file_name_vid()
        vid = "raspivid -t 0 -o /home/pi/"+videoFile+" -rot 270"
        subprocess.Popen(vid, shell=True)
        vout.say("Taking Video")
        line_prepender("vidfiles.txt", videoFile)
    if "STOP" in phrase.upper() and "VIDEO" in phrase.upper():
        kill = "killall raspivid"
        subprocess.Popen(kill, shell=True)
        vout.say("Stopped Video")
    if "RUN" in phrase.upper() and "PROGRAM" in phrase.upper():
        runprog = "sudo python /home/pi/piglass/PiGlassBeta.py"
        subprocess.Popen(runprog, shell=True)
    if "SHOW" in phrase.upper() and "VIDEO" in phrase.upper():
	with open('vidfiles.txt', 'r') as f:
                first_line = f.readline()

        print first_line
        first_line = first_line.strip('\n')
        player = "omxplayer /home/pi/"+first_line
        subprocess.Popen(player, shell=True)
    if "SHOW" in phrase.upper() and "PICTURE" in phrase.upper():
        with open('picfiles.txt', 'r') as f:
	    	first_line = f.readline()

	print first_line
        first_line = first_line.strip('\n')

	viewer = "sudo fbi -a -T 2 /home/pi/"+first_line
	subprocess.Popen(viewer, shell=True)

	time.sleep(10)
	killviewer = "sudo killall fbi"
	subprocess.Popen(killviewer, shell=True)
#	img1 = cv2.imread('/home/pi/'+first_line)
#	cv2.imshow('Last Picture',img1)
#	time.sleep(10)
#	cv2.destroyAllWindows()

#while True:
#    pass

judy.listen(vin, vout, handle, callsign='Pi', attention_span=10, forever=True)
#while True:
#    if running == True:
#	print "running on"
#        judy.listen(vin, vout, handle, callsign='Pi', attention_span=10, forever=True, running=True)
#    else:
#	#break

#	print "running off"
#	kill = "sudo killall pocketsphinx_continuous"
#        subprocess.Popen(kill, shell=True)
#	judy.listen(None, None, None, callsign='Pi', attention_span=0, forever=False, running=False)
#	judy.listen(None, None, None, callsign=None, attention_span=None, forever=False)
