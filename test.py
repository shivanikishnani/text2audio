from receiver import *
from sender import *
import itertools
from time import sleep
from scipy import stats

test_chars = 1000 # test parameter: number of characters you want to hear.
# lead = 0.2 # experimental parameter: the observed time taken by garbage characters before message starts.
lag = 0.25 # experimental parameter: the observed time by which listening lags behind hearing the message.
show = True # if you want to show the message being sent and received in parallel
splitter = int(1024 / CHUNK) # the number of sub-intervals CHARTIME gets split into.

if __name__ == "__main__":
    stream, audio = start_listening()
    message = "the five boxing wizards jump quickly"
    received = [] 

    for char in message[:test_chars]:
        play(char)
        avg = []
        for _ in range(splitter):
            avg.append(read_from_stream(stream, CHARTIME / splitter))

        chars = [decode_frame(f) for f in avg]
        print(''.join(chars))
        char_received = chr(int(np.round(stats.mode(np.vectorize(ord)(chars))[0]))) 
        # this is a disgusting number of function calls just to average a list of characters
        received.append(char_received)
        if show:
            print(char, char_received)

    for _ in range(int(lag / CHARTIME)):
        avg = []
        for _ in range(splitter):
            avg.append(read_from_stream(stream, CHARTIME / splitter))

        chars = [decode_frame(f) for f in avg]
        print(''.join(chars))
        char_received = chr(int(np.round(stats.mode(np.vectorize(ord)(chars))[0]))) 
        # this is a disgusting number of function calls just to average a list of characters
        received.append(char_received)
        if show:
            print(' ', char_received)

    stop_listening(stream, audio)
    print(''.join(received).strip())
    