# Calibration of the sound levels.

from utils import *
from sender import *
from receiver import *
import numpy as np
from matplotlib import pyplot as plt

def band_sine(f, spread):
    freqs = np.arange(f - spread, f + spread)
    return sum([sine(freq, d)[1000:] for freq in freqs])

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
    freqsets_to_test = [[all_freqs[i + k] for i in [0, 1, 3, 4]] for k in list(range(10, 15)) * 2]

    colors = ['k']

    ambient_time = read_from_stream(listen_stream, 10 * d)
    ambient_freqs, ambient_power = get_psd(ambient_time)

    to_concatenate = list(sum([band_sine(f, step / 2) for f in freqs]) for freqs in freqsets_to_test)
    combined_message = np.concatenate(to_concatenate)
    
    if True:
        plt.plot(combined_message)
        plt.show()

    send_stream.write(combined_message.astype(np.float32).tostring())
    heard_total = read_from_stream(listen_stream, 50 * d)

    k = int(len(heard_total) / len(freqsets_to_test))

    plt.plot(get_waveform(heard_total))
    plt.show()

    heard_list = []
    for i in range(len(freqsets_to_test)):
        heard_list.append(heard_total[k * i: k * (i + 1)])

    for i, heard in enumerate(heard_list):
        f, p = get_psd(heard)
        p -= ambient_power
        middle = (highest - lowest) / 2 + lowest
        spread = middle - lowest
        
        plt.semilogy(f[np.abs(f - middle) < spread], p[np.abs(f - middle) < spread], label=str(i))

        for f in freqsets_to_test[i]:
            plt.axvline(x=f, color=colors[i % len(colors)])

        #plt.show()

    stop_sending(send_stream, send_audio)
    stop_listening(listen_stream, listen_audio)
