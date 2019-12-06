import numpy as np
import pyaudio
import math
from encoder import * 
import pdb

total_freqs = 0
k_peaks = 0
time_interval = 0
message_size = np.log2(total_freqs / min_freq) #per time interval

def window_an_array(message_list, trip_window=3, windowing=True):
	final_list = [[0]*5] * 2
	final_list.append([[0] * 5] * 2)
	length = len(message_list)
	pdb.set_trace()
	for i, char_list in enumerate(message_list):
		if i < length - 2:
			first = message_list[i]
			second = message_list[i + 1]
			third = message_list[i + 2]
		final_list.append(first, second, third)
		
	final_list.append(message_list[i], final_list.message_list[i + 1])
	final_list.append([[0] * 5] * 2)
	


def encode_peaks(message):
    '''
    Cleans the message, convert characters to bits, 
    onvert message to bits 
    find floor fo log_2 (k)
    '''
    bin_message = window_an_array([char_to_bin(c) for c in clean(message)])

 

if __name__ == "__main__":
	encode_peaks("heheheh")