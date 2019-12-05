import pyaudio
import wave
import numpy as np
from scipy import signal
from matplotlib import pyplot as plt
from coder import *
from utils import *

def read_from_stream(stream, time):
    frames = []
    for _ in range(int(RATE / CHUNK * time)):
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)

    return frames

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


def get_psd(frames):
    '''
    Takes in frames from listen, and converts them back to the frequencies identified.
    Some code from https://pythonfundu.blogspot.com/2019/03/realtime-audio-visualization-in-python.html
    '''
    cleaned_frames = [np.frombuffer(frame, dtype=np.int16) for frame in frames]
    frame = np.hstack(cleaned_frames)
    freqs, power = np.fft.fftfreq(frame.shape[-1], d=1/RATE), np.abs(np.fft.fft(frame)) ** 2
    return np.fft.fftshift(freqs), np.fft.fftshift(power)

def get_frequencies(frames):
    '''
    Takes in frames, gets their PSD, and returns the corresponding frequencies to be decoded by coder.decode.
    '''
    freqs, power = get_psd(frames)
    inds = signal.find_peaks(power, height=0.1 * max(power))[0]
    print(inds)
    for i in inds:
        # try and find close to a 1-2-4 group
        for candidate in [2 * i - 1, 2 * i, 2 * i + 1, 4 * i - 1, 4 * i, 4 * i + 1]:
            if candidate in inds:
                return freqs[i]
                
    return min(inds)

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
    listen_stream, listen_audio = start_listening()
    for _ in range(50):
        opinions.append(decode_frame(read_from_stream(listen_stream, CHARTIME)))
    stop_listening(listen_stream, listen_audio)
    print(''.join(opinions))
