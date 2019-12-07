import numpy as np
import pyaudio
from scipy.special import comb

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 40000
CHUNK = 1000
pop = 0 # number of timesteps to reject initially to avoid pops

lowest = 200
highest = 1950
step = 50
d = 0.1

middle = (lowest + highest) / 2
spread = middle - lowest

total_freqs = 33
k_peaks = 4
modality = 3 # number of peaks actually seen on the PSD per peak sent

message_size = int(np.ceil(np.log2(comb(total_freqs, k_peaks))))

def start_sending():
    '''
    Open the pyaudio stream from the sender side.
    I essentially took this and play from https://github.com/lneuhaus/pysine/blob/master/pysine/pysine.py
    '''
    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paFloat32, channels=1, rate=RATE, output=1)
    return stream, audio

def stop_sending(stream, audio):
    stream.stop_stream()
    stream.close()
    audio.terminate()

def start_listening():
    '''
    Open the pyaudio stream from the listener side.
    '''
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    return stream, audio

def stop_listening(stream, audio):
    stream.stop_stream()
    stream.close()
    audio.terminate()

def sine(frequency, length):
  length = int(length * RATE)
  factor = float(frequency) * (np.pi * 2) / RATE
  return np.sin(np.arange(length) * factor)

def band_sine(f, modal_spread):
    freqs = np.linspace(f - modal_spread, f + modal_spread, num=modality, endpoint=True)
    if modality == 1:
        volumes = [1]
    elif modality == 2:
        volumes = [1, 1]
    elif modality == 3:
        volumes = [1, 2, 1]
    return sum([sine(freq, d) * volumes[i] for i, freq in enumerate(freqs)])
