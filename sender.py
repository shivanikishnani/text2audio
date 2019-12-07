# Sender-side methods.

import pyaudio
import wave
import numpy as np
from encode_k import *
from time import sleep
from matplotlib import pyplot as plt
from scipy import signal
from utils import * 
from copy import deepcopy

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
    permuted_chunks = encode_peaks(message) #list of peak arrays 
    chunks_to_play = []
    for p in permuted_chunks:
        chunks_to_play.append(get_sound_to_play(p))

    return np.concatenate(chunks_to_play)

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

if __name__ == "__main__":
    stream, audio = start_sending()
    play_alphabet(stream)
    stop_sending(stream, audio)    
