# Sender-side methods.

import pyaudio
import wave
import numpy as np
from coder import *
from time import sleep
from matplotlib import pyplot as plt
from scipy import signal
from utils import * 
from copy import deepcopy

def sine(frequency, length):
  length = int(length * RATE)
  factor = float(frequency) * (np.pi * 2) / RATE
  return np.sin(np.arange(length) * factor)

def harmonics1(freq, length):
  a = sine(freq * 1.00, length)
  b = sine(freq * 2.00, length)
  c = sine(freq * 4.00, length)
  return (a + b + c) * 0.2

def get_chunk_for_freqs(freqs, d):
    return sum([harmonics1(f, d) for f in freqs]) / 3

def get_message_to_play(message, window):
    '''
    Takes in a text message and returns the chunk to play.
    Some inspiration from https://davywybiral.blogspot.com/2010/09/procedural-music-with-pyaudio-and-numpy.html
    '''
    encoded = encode(message)
    duration = 0
    last_f, next_f = 0, 0
    chunks = []
    for i in range(len(encoded)):
        f, d = encoded[i]
        if window and i < len(encoded) - 1:
            next_f = encoded[i + 1][0]
        if window and i > 0:
            last_f = encoded[i - 1][0]
        chunks.append(get_chunk_for_freqs([last_f, f, next_f], d))

    return np.concatenate(chunks)

def play(message, stream, window=False):
    '''
    Plays a message as returned by get_message_to_play.
    '''
    chunk = get_message_to_play(message, window)
    stream.write(chunk.astype(np.float32).tostring())

def show_expected_psd(char):
    '''
    Takes in a character and plots the PSD we expect to get from hearing it.
    '''
    f = mappings[char]
    chunk = get_chunk_for_freqs([0, f, 0], CHARTIME)
    f, p = signal.periodogram(chunk, fs=RATE)
    plt.plot(f[:100], p[:100])
    plt.title("Character: " + char)
    plt.show()

def play_alphabet(stream):
    return play("abcdefghijklmnopqrstuvwxyz. ", stream)
    
