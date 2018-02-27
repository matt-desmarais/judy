import judy
import datetime
import subprocess

vin = judy.VoiceIn(adcdev='plughw:1,0',
                   lm='/home/pi/judy/7470.lm',
                   dict='/home/pi/judy/7470.dic')

vout = judy.VoiceOut(device='plughw:0,0',
                     resources='/home/pi/judy/resources/audio')

def get_file_name_pic():  # new
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")

def get_file_name_vid():  # new
    return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")

def handle(phrase):
    print 'Heard:', phrase
    vout.say(phrase)
    if "TAKE" in phrase.upper() and "PICTURE" in phrase.upper():
        filename = get_file_name_pic()
        photo = "raspistill -o /home/pi/"+filename+" -rot 270"
        subprocess.Popen(photo, shell=True)
    if "TAKE" in phrase.upper() and "VIDEO" in phrase.upper():
        videoFile = get_file_name_vid()
        vid = "raspivid -t 0 -o /home/pi/piglass/"+videoFile+" -rot 270"
        subprocess.Popen(vid, shell=True)
    if "STOP" in phrase.upper() and "VIDEO" in phrase.upper():
        kill = "killall raspivid"
        subprocess.Popen(kill, shell=True)

#while True:
judy.listen(vin, vout, handle, callsign='Pi', attention_span=10, forever=True)
