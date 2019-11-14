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

if __name__ == "__main__":
    print(play("Software-defined radio (SDR) is a radio communication system where components that have been traditionally implemented in hardware (e.g. mixers, filters, amplifiers, modulators/demodulators, detectors, etc.) are instead implemented by means of software on a personal computer or embedded system.[1] While the concept of SDR is not new, the rapidly evolving capabilities of digital electronics render practical many processes which were once only theoretically possible."))
    