from receiver import *
from sender import *
import itertools
from time import sleep

test_chars = 1000 # test parameter: number of characters you want to hear.
lead = 0.1 # experimental parameter: the observed time taken by garbage characters before message starts.
lag = 0.25 # experimental parameter: the observed time by which listening lags behind hearing the message.
show = False # if you want to show the message being sent and received in parallel

if __name__ == "__main__":
    stream, audio = start_listening()
    message = "the five boxing wizards jump quickly."
    received = []

    for char in message[:test_chars]:
        # I feel like there might be a bug here because of synchronization: it might stop listening before I start playing.
        # Won't be an issue when actually running things, though.
        play(char)
        heard = read_from_stream(stream, CHARTIME)
        char_received = decode_frame(heard)
        received.append(char_received)
        if show:
            print(char, char_received)

    for _ in range(int(lag / CHARTIME)):
        heard = read_from_stream(stream, CHARTIME)
        char_received = decode_frame(heard)
        received.append(char_received)
        if show:
            print(' ', decode_frame(heard))

    stop_listening(stream, audio)
    print(''.join(received))
    