from receiver import *
from new_sender import *
from decode import *
import itertools
from time import sleep
from scipy import stats
from matplotlib import pyplot as plt

test_chars = 1000 # test parameter: number of characters you want to hear.
lead = 0.2 # experimental parameter: the observed time taken by garbage characters before message starts.
lag = 0.25 # experimental parameter: the observed time by which listening lags behind hearing the message.


if __name__ == "__main__":
    listen_stream, listen_audio = start_listening()
    send_stream, send_audio = start_sending()
    message = "hello world."

    for _ in range(int(lead / CHARTIME)):
        read_from_stream(listen_stream, CHARTIME)    

    for char in message[:test_chars]:
        # I feel like there might be a bug here because of synchronization: it might stop listening before I start playing.
        # Won't be an issue when actually running things, though.
        play(char, send_stream)
        
        freqs, powers = get_psd(read_from_stream(listen_stream, CHARTIME))
        sound_data = (freqs, powers)
        process_sound_from_stream(sound_data, decode_sound)

    for _ in range(int(lag / CHARTIME)):
        freqs, powers = get_psd(read_from_stream(listen_stream, CHARTIME))
        sound_data = (freqs, powers)
        process_sound_from_stream(sound_data, decode_sound)
        

    stop_listening(listen_stream, listen_audio)
    stop_sending(send_stream, send_audio)
    plt.show()
    