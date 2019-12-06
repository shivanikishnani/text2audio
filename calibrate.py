# Calibration of the sound levels.

from utils import *
from sender import *
from receiver import *
import numpy as np
from matplotlib import pyplot as plt

lowest = 100
highest = 2100
step = 30
d = 0.3

def band_sine(f, spread):
    freqs = np.arange(f - spread, f + spread, 5)
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
    freqsets_to_test = [all_freqs[:5]]

    colors = ['k']

    for i, freqs in enumerate(freqsets_to_test):
        to_send = sum([band_sine(f, 10) for f in freqs])

        ambient_time = read_from_stream(listen_stream, d)
        ambient_freqs, ambient_power = get_psd(ambient_time)

        send_stream.write(to_send.astype(np.float32).tostring())
        heard = read_from_stream(listen_stream, d)
        f, p = get_psd(heard)
        p -= ambient_power
        middle = (highest + step - lowest) / 2
        spread = middle + step - lowest # I think
        plt.semilogy(f[np.abs(f - middle) < spread], p[np.abs(f - middle) < spread], label=str(i))

        for f in freqs:
            plt.axvline(x=f, color=colors[i % len(colors)])

        plt.show()
        sleep(0.5)

    stop_sending(send_stream, send_audio)
    stop_listening(listen_stream, listen_audio)