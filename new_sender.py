# Sender-side methods.

import pyaudio
import wave
import numpy as np
from encoder import *
from time import sleep
from matplotlib import pyplot as plt
from scipy import signal

window = 3

def start_sending():
    '''
    Open the pyaudio stream from the sender side.
    I essentially took this and play from https://github.com/lneuhaus/pysine/blob/master/pysine/pysine.py
    '''
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)
    return stream, audio

def sine(frequency, length):
  length = int(length * RATE)
  factor = float(frequency) * (np.pi * 2) / RATE
  return np.sin(np.arange(length) * factor)

def harmonics1(freq, length):
  a = sine(freq * 1.00, length)
  b = sine(freq * 2.00, length)
  c = sine(freq * 4.00, length)
  return (a + b + c) * 0.2

def play_triple(triple, power, length):
    a = sine(triple[0] * power[0], length)
    b = sine(triple[1] * power[1], length)
    c = sine(triple[2] * power[2], length)
    return (a + b + c)

def get_chunk_for_freqs(freqs, d):
    return sum([harmonics1(f, d) for f in freqs]) / 3

def get_chunk_for_triples(triples, powers, length):
    return sum([play_triple(triples[i], powers[i], length)] for i in range(len(triples))) / 3

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

def new_get_message_to_play(message):
    encoded = new_encode(message)
    chunks = []
    # might have obog right here
    i = 0
    while i < len(encoded):
        triples = [TRIPLES[j] for j in range(i, i + WINDOW) if encoded[j]]
        powers = [POWERS[j] for j in range(i, i + WINDOW) if encoded[j]]
        chunks.append(get_chunk_for_triples(triples, powers, CHARTIME))
        i += SHIFT

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

def stop_sending(stream, audio):
    stream.stop_stream()
    stream.close()
    audio.terminate()

def play_alphabet(stream):
    return play("abcdefghijklmnopqrstuvwxyz. ", stream)

if __name__ == "__main__":
    '''for char in "c":
        show_expected_psd(char)'''
    stream, audio = start_sending()
    play("hello world", stream)
    stop_sending(stream, audio)