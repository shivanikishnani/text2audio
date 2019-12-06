import numpy as np
import pyaudio
import math
import pdb
import doctest
from utils import *
from scipy.special import comb

"""
letter messages (str) -> (str2str) windowed messages ->  (str2str) bits -> 
(str2listofstr_) message_size chunks of bits
 -> (str_2array) an array of peaks locations corresponding to each chunk
""" 

message_size = int(np.log2(comb(total_freqs, k_peaks)))

def window_an_array(message_list, trip_window=3, windowing=True):
	final_list = [[0]*5] * 2
	length = len(message_list) 
	message_list = [[0]* 5] * 2 + message_list
	for i, char_list in enumerate(message_list):
		if i < length - 2:
			first = message_list[i]
			second = message_list[i + 1]
			third = message_list[i + 2]
		else:
			first = message_list[i]
			second = message_list[i + 1]
			third = [0] * 5
		final_list.append([first, second, ])
		final_list.append(second)
		final_list.append(third)
		if sum(third) == 0:
			break
	final_list.append([0] * 5)
	print(final_list)
	# final_list.append(message_list[i], final_list.message_list[i + 1])
	return final_list

def window_str(message, window_size=3, windowing=True):
	"""
	str message -> windowed str message
	
	>>>window_str("abc")
	"00a0ababcbc0c00"
	>>>window_str("a")
	"00a0a0a00"
	"""
	length = len(message)
	final_message = ""

	if not windowing:
		window_size = 1
	else: 
		message = "00" + message
		length += 2

	for i in range(length):
		
		win = message[i : i + window_size]
		win = win + "0" * (window_size - len(win))

		final_message += win
	return final_message


def char_to_ind(char):
    if 97 <= ord(char) <= 122:
        return ord(char) - 97
    elif char == ' ':
        return 26
    else:
        return 27

def char_to_bin(char):
    lst = [str(int(c)) for c in np.binary_repr(char_to_ind(char) + 1)]
    while len(lst) < 5:
        lst.extend(str(0))
    bin_str = ""
    bin_str = bin_str.join(lst)
    return bin_str

def ind_to_char(ind):
    if 0 <= ind < 26:
        return chr(ind + 97)
    elif ind == 27:
        return chr(46)
    return chr(32)

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

def encode_peaks(message):
    '''
    Cleans the message, convert characters to bits, 
    onvert message to bits 
    find floor fo log_2 (k)
    '''
    window_message = window_str(clean(message))
    window_bits = "".join([char_to_bin(c) for c in window_message])
    #divide it into chunks
    chunk_bits = [window_bits[i:i+message_size] for i in range(0, len(window_bits), message_size)]
    print(chunk_bits)
 
def band_sine(f, spread):
    freqs = np.arange(f - spread, f + spread)
    return sum([sine(freq, d)[1000:] for freq in freqs])

def get_frequencies()

if __name__ == "__main__":
	encode_peaks("hello world")
