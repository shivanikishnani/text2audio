# Sender-side methods.

import pyaudio
import wave
import pysine
from coder import *
 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
 
def play(message):
    encoded = encode(message)
    duration = 0
    for f, d in encoded:
        pysine.sine(f, d)
        duration += d
    return round(duration, 2)

def play_alphabet():
    play("abcdefghijklmnopqrstuvwxyz. ")

if __name__ == "__main__":
    play_alphabet()
