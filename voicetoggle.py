import subprocess
import RPi.GPIO as GPIO

global running
running = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def toggleVoiceCommands(channel):
    global running
    if running == 0:
	print "starting voice commands"
	subprocess.Popen(["aplay", "/home/pi/judy/enabled.wav"])
    	subprocess.Popen(["sudo python /home/pi/judy/testjudy.py"], shell=True)
	running = 1
    elif running == 1:
	print "stopping voice commands"
        subprocess.Popen(["sudo pkill -9 -f testjudy.py"], shell=True)
	running = 0
	subprocess.Popen(["aplay", "/home/pi/judy/disabled.wav"])

GPIO.add_event_detect(20, GPIO.FALLING, callback=toggleVoiceCommands, bouncetime=300)

while True:
    pass
