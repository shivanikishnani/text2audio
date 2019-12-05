# Calibration of the sound levels.

from utils import *
from sender import *
from receiver import *
import numpy as np
from matplotlib import pyplot as plt

lowest = 50
highest = 2000
step = 100
d = 0.1

def calibrate():
    send_stream, send_audio = start_sending()
    listen_stream, listen_audio = start_listening()

    freqs = np.arange(lowest, highest + step, step)
    scales = np.zeros(freqs.shape)

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
        scales[i] = max(powers) / avg_power
        print(scales[i])

    np.save('./scaling_' + str(lowest) + '_' + str(highest) + '_' + str(step) + '.npy', scales)

if __name__ == "__main__":
    try:
        scales = np.load('./scaling_' + str(lowest) + '_' + str(highest) + '_' + str(step) + '.npy')
    except FileNotFoundError:
        calibrate()
        scales = np.load('./scaling_' + str(lowest) + '_' + str(highest) + '_' + str(step) + '.npy')
    send_stream, send_audio = start_sending()
    listen_stream, listen_audio = start_listening()
    all_freqs = np.arange(lowest, highest + step, step)
    freqs1 = all_freqs[:2] # np.arange(lowest, highest + step, step * 2)
    freqs2 = all_freqs[:5]
    d = 0.1

    for freqs in [freqs1, freqs2]:
        to_send = sum([sine(f, d) * scales[np.where(all_freqs == f)] ** 1 for f in freqs])
        
        send_stream.write(to_send.astype(np.float32).tostring())
        heard = read_from_stream(listen_stream, d)
        f, p = get_psd(heard)
        middle = (highest + step - lowest) / 2
        spread = middle + step - lowest # I think
        plt.semilogy(f[np.abs(f - middle) < spread], p[np.abs(f - middle) < spread])

        for f in freqs:
            plt.axvline(x=f, color='k')

    stop_sending(send_stream, send_audio)
    stop_listening(listen_stream, listen_audio)

    plt.show()