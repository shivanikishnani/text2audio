# Encoding and decoding methods.

import numpy as np

CHARTIME = 0.05
min_freq = 20
mappings = {i: round(min_freq * pow(2, i/13), 3) for i in range(128)} # ascii, step size is a semitone

def encode(message, charlength=CHARTIME):
    '''
    Encodes a message (str) according to a currently very primitive scheme.
    Returns a set of tuples (freq, duration) to be passed into 'transmit'.
    Currently all durations are 0.1 seconds even though that doesn't meet the bitrate.
    '''
    return [(mappings[ord(c)], charlength) for c in message]

def decode(f):
    '''
    Takes in a frequency and returns the best (MAP/MLE eventually?) guess of what the corresponding character is.
    '''
    return chr(int(round(np.log2(f / min_freq) * 13)))
    