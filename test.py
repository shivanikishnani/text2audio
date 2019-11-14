from receiver import *
from sender import *
import itertools
from time import sleep

test_chars = 1000 # test parameter: number of characters you want to hear.
lead = 0.1 # experimental parameter: the observed time taken by garbage characters before message starts.
lag = 0.2 # experimental parameter: the observed time by which listening lags behind hearing the message.

if __name__ == "__main__":
    stream, audio = start_listening()
    message = "hello world"
    heard = []
    for char in message[:test_chars]:
        # I feel like there might be a bug here because of synchronization: it might stop listening before I start playing.
        # Won't be an issue when actually running things, though.
        play(char)
        heard.append(read_from_stream(stream, CHARTIME))
    
    for _ in range(int(lag / CHARTIME) + 1):
        heard.append(read_from_stream(stream, CHARTIME))

    heard = heard[int(lead / CHARTIME):]
    stop_listening(stream, audio)
    print(decode_framesets(heard))
    