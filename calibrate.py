# Calibration of the sound levels.

from utils import *
from sender import *
from receiver import *
import numpy as np
from matplotlib import pyplot as plt

if __name__ == "__main__":
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
