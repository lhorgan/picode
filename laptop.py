import RPi.GPIO as GPIO
from time import sleep
import requests

from pydub import AudioSegment
from pydub.playback import play

song_p1 = AudioSegment.from_wav("./can_song_p1.wav")
song_p2 = AudioSegment.from_wav("./can_song_p2.wav")
   
SERVER_URL = "http://3.19.213.203:6081"

PLAY_SONG = False

try:
    while True:
        r = requests.get(f"{SERVER_URL}/status")
        if status == "play_song" and not PLAY_SONG:
            PLAY_SONG = True
            play(song_p1)
            sleep(6)
            play(song_p2)
            break