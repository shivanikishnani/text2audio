from receiver import *
from sender import *
import itertools
from time import sleep
from scipy import stats

test_chars = 1000 # test parameter: number of characters you want to hear.
lead = 0.25 # experimental parameter: the observed time taken by garbage characters before message starts.
lag = 0.25 # experimental parameter: the observed time by which listening lags behind hearing the message.
show = False # if you want to show the message being sent and received in parallel

if __name__ == "__main__":
    listen_stream, listen_audio = start_listening()
    send_stream, send_audio = start_sending()
    message = "abcdefghijklmnopqrstuvwxyz. "
    received = []

    ambient = read_from_stream(listen_stream, CHARTIME)
    ambient_decoded = [np.frombuffer(frame, dtype=np.int16) for frame in ambient]

    _, ambient_power = signal.periodogram(np.hstack((ambient_decoded)), fs=RATE)

    for _ in range(int(lead / CHARTIME)):
        read_from_stream(listen_stream, CHARTIME)    
    
    play(message, send_stream)
    heard = read_from_stream(listen_stream, CHARTIME * len(message))
    k = int(len(heard) / len(message))

    for i in range(len(message)):
        heard_window = heard[k * i: k * (i + 1)]
        frame = clean_frame(heard_window)
        psdfreqs, power = signal.periodogram(frame, fs=RATE)
        plt.semilogy(psdfreqs, power)
        plt.show()
        char_received = decode_frame(heard_window, ambient_power)
        received.append(char_received)
        if show:
            print(char, char_received)

    stop_listening(listen_stream, listen_audio)
    stop_sending(send_stream, send_audio)
    print(''.join(received)[1:])
    