import pyaudio
import wave
import numpy as np
from encoder import *
from scipy import signal
from matplotlib import pyplot as plt
from utils import *
from decode_k import decode, five_to_letter

def read_from_stream(stream, time):
    frames = []
    for _ in range(int(RATE / CHUNK * time)):
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)

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

def get_windowed_psd(waveform):
    if isinstance(waveform, str):
        waveform = np.load(waveform)

    heard_list = []
    num_windows = int(len(waveform) / (RATE * d))
    k = len(waveform) // num_windows

    for i in range(num_windows):
        heard_list.append(get_waveform(waveform[k * i: k * (i + 1)]))

    psds = []
    for i, heard in enumerate(heard_list):
        f, p = get_psd(heard)
        psds.append(p)

    # resampling

    f_desired = np.fft.fftfreq(int(RATE * d), d = 1 / RATE)
    f_desired = f_desired[np.abs(f_desired - middle) <= spread]

    return f, psds

def convert_to_str(bitstr):
    # 5 for each char
    message = ""
    for i in range(0, len(bitstr), 5):
        message += five_to_letter(bitstr[i: i + 5])
    return message

def listen_and_decode(listen_time):
    listen_stream, listen_audio = start_listening()
    frames = read_from_stream(listen_stream, listen_time)
    stop_listening(listen_stream, listen_audio)

    heard = get_waveform(frames)
    f, psds = get_windowed_psd(heard)
    middle = (lowest + highest) / 2
    spread = middle - lowest
    
    for i, p in enumerate(psds):
        psds[i] = p[np.abs(f - middle) <= spread]
        plt.semilogy(f[np.abs(f - middle) <= spread], psds[i])
        
    f = f[np.abs(f - middle) <= spread]
    full_bit_msg = ''.join([decode(p) for p in psds])
    full_str_msg = convert_to_str(full_bit_msg)
    return full_str_msg

def temp_func(psds):
    full_bit_msg = ''.join([decode(p) for p in psds])
    print("final bit message:", full_bit_msg)
    full_str_msg = convert_to_str(full_bit_msg)
    print("final message:" , full_str_msg)

if __name__ == "__main__":
    print(listen_and_decode(0.1))
    # temp_func([[27, 30, 31, 32], [18, 23, 28, 32]])
