# Encoding and decoding methods.

import numpy as np

CHARTIME = 0.05
min_freq = 440
log_step = 7
mappings = {i: round(min_freq * pow(2, i / log_step), 3) for i in range(28)}

def clean(message):
    '''
    Takes in a message and cleans it so that it only has a-z, spaces, and periods.
    I feel like there's a more efficient implementation of this.
    '''
    cleaned_message = []
    for c in message:
        if c.isalpha():
            cleaned_message.append(c.lower())
        elif not c.isalpha() and c not in [' ', '.']:
            cleaned_message.append(' ')

    return ''.join(cleaned_message)

def char_to_ind(char):
    if 97 <= ord(char) <= 122:
        return ord(char) - 97
    elif char == ' ':
        return 26
    else:
        return 27

def ind_to_char(ind):
    if 0 <= ind < 26:
        return ind + 97
    elif ind == 27:
        return 46
    return 32

def encode(message, charlength=CHARTIME):
    '''
    Encodes a message (str) according to a currently very primitive scheme.
    Returns a set of tuples (freq, duration) to be passed into 'transmit'.
    Currently all durations are 0.1 seconds even though that doesn't meet the bitrate.
    '''
    return [(mappings[char_to_ind(c)], charlength) for c in clean(message)]

def decode(f):
    '''
    Takes in a frequency and returns the best (MAP/MLE eventually?) guess of what the corresponding character is.
    '''
    return chr(ind_to_char(int(round(np.log2(f / min_freq) * log_step))))
