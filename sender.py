# Sender-side methods.

import pyaudio
import wave
import numpy as np
from coder import *

window = 3

def start_sending():
    '''
    Open the pyaudio stream from the sender side.
    I essentially took this and play from https://github.com/lneuhaus/pysine/blob/master/pysine/pysine.py
    I wanted to just import pysine, but then wanted more customization.
    '''
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.get_format_from_width(1), channels=CHANNELS,
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
        times = np.linspace(0, d, int(RATE * d), endpoint=False)
        stream.write(np.array((np.sin(times * f * 2 * np.pi) + 1.0) * 127.5, dtype=np.int8).tostring())
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
