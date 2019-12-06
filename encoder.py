# Encoding and decoding methods.
# Also a collection for dependencies. Probably not a good design idea.

import numpy as np
import pyaudio
import math

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

CHARTIME = 0.05
min_freq = 220
log_step = 10

START = 100
END = 2100
INC = 50
WINDOW = (END - START) // (INC * 3)
SHIFT = int(math.floor(WINDOW / 3))

arr = list(range(START, END + INC, INC))
# 3 unique frequencies per index (lazy coding, could be redone)
TRIPLES = {i: (arr[3 * i], arr[3 * i + 1], arr[3 * i + 2]) for i in range(WINDOW)}
# for adjusting power of frequency, placeholder
POWERS = {i: (1.00, 1.00, 1.00) for i in range(WINDOW)}


def char_to_ind(char):
    if 97 <= ord(char) <= 122:
        return ord(char) - 97
    elif char == ' ':
        return 26
    else:
        return 27

def char_to_bin(char):
    lst = [int(c) for c in np.binary_repr(char_to_ind(char) + 1)]
    while len(lst) < 5:
        lst.insert(0, 0)
    return lst

def ind_to_char(ind):
    if 0 <= ind < 26:
        return chr(ind + 97)
    elif ind == 27:
        return chr(46)
    return chr(32)

mappings = {ind_to_char(i): round(min_freq * pow(2, i / log_step), 7) for i in range(28)}

def clean(message):
    '''
    Takes in a message and cleans it so that it only has a-z, spaces, and periods.
    I feel like there's a more efficient implementation of this.
    '''
    cleaned_message = []
    for c in message:
        if c.isalpha():
            cleaned_message.append(c.lower())
        elif not c.isalpha() and c != '.':
            cleaned_message.append(' ')
        else:
            cleaned_message.append('.')

    return ''.join(cleaned_message)

def encode(message, charlength=CHARTIME):
    '''
    Encodes a message (str) according to a currently very primitive scheme.
    Returns a set of tuples (freq, duration) to be passed into 'transmit'.
    Currently all durations are 0.1 seconds even though that doesn't meet the bitrate.
    '''
    return [(mappings[c], charlength) for c in clean(message)]

def new_encode(message):
    lst = []
    for _ in range(WINDOW - SHIFT):
        lst.append(0)
    for c in clean(message):
        lst.extend(char_to_bin(c))
    for _ in range(WINDOW - SHIFT):
        lst.append(0)
    return lst

def decode(f):
    '''
    Takes in a frequency and returns the best (MAP/MLE eventually?) guess of what the corresponding character is.
    '''
    return ind_to_char(int(round(np.log2(f / min_freq) * log_step)))
