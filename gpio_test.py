import RPi.GPIO as GPIO
from time import sleep
import requests

from pydub import AudioSegment
from pydub.playback import play

song_p1 = AudioSegment.from_wav("/home/pi/Music/can_song_p1.wav")
song_p2 = AudioSegment.from_wav("/home/pi/Music/can_song_p2.wav")

PICKED_UP_PIN = 4
OPEN_BOX_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(PICKED_UP_PIN, GPIO.IN)
GPIO.setup(OPEN_BOX_PIN, GPIO.OUT, initial=GPIO.LOW)
   
SERVER_URL = "http://3.19.213.203:6081"

ARMED = False
PICKED_UP = False

try:
    i = 0

    while True:
        i += 1
        print(GPIO.input(PICKED_UP_PIN))

        if i % 5 == 0:
            try:
                r = requests.get("%s/pi_alive" % SERVER_URL)
            except:
                pass
        # if not ARMED:
        try:
            r = requests.get("%s/armed" % SERVER_URL)
            print(r.text)
            if r.text == "true":
                ARMED = True
            else:
                ARMED = False
        except:
            pass
        if ARMED:
            if not GPIO.input(PICKED_UP_PIN): # push button released
                r = requests.get(f"{SERVER_URL}/set_play_song")
                print("Box has been picked up")
                sleep(173)
                #play(song_p1)
                GPIO.output(OPEN_BOX_PIN, GPIO.HIGH)
                #sleep(6)
                #play(song_p2)
                break
        #print(GPIO.input(4))
        sleep(0.5)
finally:
    GPIO.cleanup()