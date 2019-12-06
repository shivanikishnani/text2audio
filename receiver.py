import pyaudio
import wave
import numpy as np
from encoder import *
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

def get_waveform(frames):
    '''
    Takes in frames from listen, and returns the time-domain data observed.
    '''
    cleaned_frames = [np.frombuffer(frame, dtype=np.int16) for frame in frames]
    frame = np.hstack(cleaned_frames)
    return frame


def get_psd(frames):
    '''
    Takes in frames from listen, and converts them back to the frequencies identified.
    Some code from https://pythonfundu.blogspot.com/2019/03/realtime-audio-visualization-in-python.html
    '''
    frame = get_waveform(frames)
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

#if we are windowing, TRIPLES must have length divisible by 3
def decode_sound(sound_data):
    freqs = sound_data[0]
    powers = sound_data[1]
    bits = [nth_bit(n, freqs, powers) for n in range(len(TRIPLES))]
    return "".join(bits)

def nth_bit(n, freqs, powers):
    freqs = list(freqs)
    threshold = "idk lol"
    bit = '1'
    for freq in TRIPLES[n]:
        ind = freqs.index(freq)
        if(powers[ind] < threshold):
            bit = '0'
    return bit

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

def get_windowed_psd(waveform, d=0.1):
    if isinstance(waveform, str):
        waveform = np.load(waveform)

    heard_list = []
    num_windows = int((len(waveform) / RATE) / d)
    k = len(waveform) // num_windows

    for i in range(num_windows):
        heard_list.append(waveform[k * i: k * (i + 1)])

    psds = []
    for i, heard in enumerate(heard_list):
        f, p = get_psd(heard)
        psds.append(p)
    
    return f, psds

if __name__ == "__main__":
    d = 0.1
    listen_time = 20
    listen_stream, listen_audio = start_listening()
    ambient_time = read_from_stream(listen_stream, d)
    ambient_freqs, ambient_power = get_psd(ambient_time)
    frames = read_from_stream(listen_stream, listen_time)
    stop_listening(listen_stream, listen_audio)
    
    num_frames = int(listen_time / d)
    k = len(frames) // num_frames

    heard_list = []
    for i in range(num_frames):
        heard_list.append(frames[k * i: k * (i + 1)])

    plt.plot(get_waveform(frames))
    plt.show()
    np.save('./fifty_frame_today.npy', get_waveform(frames))
