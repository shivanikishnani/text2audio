# Sender-side methods.

import pyaudio
import wave
import numpy as np
from coder import *
from time import sleep
from matplotlib import pyplot as plt

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

def get_sine(f, d):
    '''
    Get a single sine of duration d and frequency f.
    '''
    times = np.linspace(0, d, int(RATE * d), endpoint=False)
    return np.array((np.sin(times * f * 2 * np.pi) + 1.0) * 127.5)
    
def get_mixed_sine(freqs, d):
    '''
    Get a mixed sine wave with an arbitrary number of frequencies.
    '''
    times = np.linspace(0, d, int(RATE * d), endpoint=False)
    toreturn = np.zeros(times.size,)
    for f in freqs:
        toreturn += np.sin(times * f * 2 * np.pi)

    return np.array((toreturn + 1.0) * 127.5)

def play(message, stream, window=False):
    '''
    Play the message according to a certain encoding.
    Some inspiration from https://davywybiral.blogspot.com/2010/09/procedural-music-with-pyaudio-and-numpy.html
    '''
    encoded = encode(message)
    duration = 0
    last_f, next_f = 0, 0
    for i in range(len(encoded)):
        f, d = encoded[i]
        if False and i < len(encoded) - 1:
            next_f = encoded[i + 1][0]
        if False and i > 0:
            last_f = encoded[i - 1][0]
        stream.write(get_mixed_sine([last_f, f, next_f], d).tostring())
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
