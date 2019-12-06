# Calibration of the sound levels.

from utils import *
from sender import *
from receiver import *
import numpy as np
from matplotlib import pyplot as plt

lowest = 200
highest = 800
step = 20
d = 0.2

def band_sine(f, spread):
    freqs = np.arange(f - spread, f + spread)
    return sum([sine(freq, d) for freq in freqs])

def calibrate(d=0.5):
    send_stream, send_audio = start_sending()
    listen_stream, listen_audio = start_listening()
    num_tests = 5

    freqs = np.arange(lowest, highest + step, step)
    scales = np.zeros(freqs.shape)

    for _ in range(num_tests):
        to_send = sum([sine(f, d) for f in freqs])
        send_stream.write(to_send.astype(np.float32).tostring())
        heard = read_from_stream(listen_stream, d)
        freqs_x, powers = get_psd(heard)
        inds = np.where(freqs_x > 0)
        freqs_x = freqs_x[inds]
        powers = powers[inds]

        for i in range(len(freqs)):
            window = np.where(np.abs(freqs_x - freqs[i]) <= step / 2)
            avg_power = np.mean(powers[window])
            scales[i] += max(powers) / avg_power

    np.save('./scaling_' + str(lowest) + '_' + str(highest) + '_' + str(step) + '.npy', scales / num_tests)

if __name__ == "__main__":
    try:
        scales = np.load('./scaling_' + str(lowest) + '_' + str(highest) + '_' + str(step) + '.npy')
    except FileNotFoundError:
        calibrate()
        scales = np.load('./scaling_' + str(lowest) + '_' + str(highest) + '_' + str(step) + '.npy')
    send_stream, send_audio = start_sending()
    listen_stream, listen_audio = start_listening()
    all_freqs = np.arange(lowest, highest + step, step)
    freqsets_to_test = [[all_freqs[i + k] for i in [0, 1, 3, 4]] for k in range(5, 10)]

    colors = ['k']

    for i, freqs in enumerate(freqsets_to_test):
        # to_send = sum([band_sine(f, step / 2) for f in freqs])
        combined_message = np.concatenate((sum([band_sine(f, step / 2) for f in freqs])))

        ambient_time = read_from_stream(listen_stream, d)
        ambient_freqs, ambient_power = get_psd(ambient_time)

        send_stream.write(to_send.astype(np.float32).tostring())
        heard = read_from_stream(listen_stream, d)
        f, p = get_psd(heard)
        p -= ambient_power
        middle = (highest - lowest) / 2 + lowest
        spread = middle - lowest
        
        plt.semilogy(f[np.abs(f - middle) < spread], p[np.abs(f - middle) < spread], label=str(i))

        for f in freqs:
            plt.axvline(x=f, color=colors[i % len(colors)])

        plt.show()

    stop_sending(send_stream, send_audio)
    stop_listening(listen_stream, listen_audio)
