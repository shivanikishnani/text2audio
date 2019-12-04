import pyaudio
import wave
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
from coder import *

def start_listening():
    '''
    Open the pyaudio stream from the listener side.
    '''
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    return stream, audio

def read_from_stream(stream, time):
    frames = []
    for _ in range(int(RATE / CHUNK * time)):
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)

    return frames

def stop_listening(stream, audio):
    stream.stop_stream()
    stream.close()
    audio.terminate()

def listen(listening_time=10, filename=None):
    '''
    Listen for listening_time (float) seconds and return the bit representation of the output.
    Optionally, for debugging, write it to filename.
    Don't run this in a while loop! start_listening creates a bit of noise at the start that I can't get rid of, so call it once for each time you actually want to start listening, not just to window out small intervals at a time.
    Modified from source https://gist.github.com/mabdrabo/8678538
    '''

    stream, audio = start_listening()
    frames = read_from_stream(stream, listening_time)
    stop_listening(stream, audio)
    
    if filename is not None:
        waveFile = wave.open(filename, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

    return frames

def get_frequencies(frames):
    '''
    Takes in frames from listen, and converts them back to the frequencies identified.
    Some code from https://pythonfundu.blogspot.com/2019/03/realtime-audio-visualization-in-python.html
    '''
    cleaned_frames = [np.frombuffer(frame, dtype=np.int16) for frame in frames]
    frame = np.hstack(cleaned_frames)
    psdfreqs, power = signal.periodogram(frame, fs=RATE)
    return psdfreqs[np.argmax(power)]

def decode_frame(frame):
    '''
    Takes in a frame and returns its decoded character.
    '''
    return decode(get_frequencies(frame))

def decode_framesets(framesets):
    '''
    Takes in a list of frames and returns its decoding.
    '''
    chars = []
    for frame in framesets:
        chars.append(decode_frame(frame))

    return ''.join(chars)

if __name__ == "__main__":
    opinions = []
    stream, audio = start_listening()
    for _ in range(50):
        opinions.append(decode_frame(read_from_stream(stream, 0.15)))

    stop_listening(stream, audio)
    print(''.join(opinions))
