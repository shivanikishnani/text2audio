# Sender-side methods.

import pyaudio
import wave
import numpy as np
from coder import *
from time import sleep
from matplotlib import pyplot as plt
from scipy import signal
from receiver import *

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

def stop_sending(stream, audio):
    stream.stop_stream()
    stream.close()
    audio.terminate()

def play_alphabet(stream):
    return play("abcdefghijklmnopqrstuvwxyz. ", stream)

if __name__ == "__main__":
    ears_bleed = False
    send_stream, send_audio = start_sending()
    listen_stream, listen_audio = start_listening()
    freqs = np.arange(50, 200, 50)
    d = 0.1
    if ears_bleed:
        freqs_sweep, power_sweep = get_psd(read_from_stream(listen_stream, d))
        power_sweep *= 0
        for f in freqs:
            to_send = sine(f, d)
            send_stream.write(to_send.astype(np.float32).tostring())
            heard = read_from_stream(listen_stream, d)
            power_sweep += get_psd(heard)[1]

    to_send = sum([sine(f, d) for f in freqs])
    print(to_send)
    plt.plot(np.linspace(0, 1, len(to_send)), to_send)
    plt.show()
    send_stream.write(to_send.astype(np.float32).tostring())
    heard = read_from_stream(listen_stream, d)
    send_stream.write(to_send.astype(np.float32).tostring())
    
    freqs_simple, power_simple = get_psd(heard)
    plt.semilogy(freqs_simple[freqs_simple > 0], power_simple[freqs_simple > 0], label="Simple")
    if ears_bleed:
        plt.semilogy(freqs_sweep[freqs_sweep > 0], power_sweep[freqs_sweep > 0], label="Sweep")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Power (unknown units)")
    plt.legend()
    '''for i in range(len(power)):
        if power[i] >= 0.25 * max(power):
            print(f[i])'''
    stop_sending(send_stream, send_audio)
    stop_listening(listen_stream, listen_audio)
    plt.show()