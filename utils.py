import numpy as np
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 40000
CHUNK = 1000

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