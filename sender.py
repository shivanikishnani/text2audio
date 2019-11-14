# Sender-side methods.

import pyaudio
import wave
import pysine
import numpy as np
from coder import *
from demo import harmonics1

def start_sending():
    '''
    Open the pyaudio stream from the sender side.
    '''
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, output=True,
                    frames_per_buffer=CHUNK)
    return stream, audio
 
def play(message, stream):
    '''
    Play the message according to a certain encoding.
    Some inspiration from https://davywybiral.blogspot.com/2010/09/procedural-music-with-pyaudio-and-numpy.html
    '''
    encoded = encode(message)
    duration = 0
    for f, d in encoded:
        stream.write(harmonics1(f, d).astype(np.float32).tostring())
        duration += d
    return round(duration, 2)

def stop_sending(stream, audio):
    stream.stop_stream()
    stream.close()
    audio.terminate()

def play_alphabet(stream):
    return play("abcdefghijklmnopqrstuvwxyz. ", stream)

if __name__ == "__main__":
    stream, audio = start_sending()
    play_alphabet(stream)
    stop_sending(stream, audio)
