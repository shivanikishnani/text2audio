import numpy as np
import pyaudio
import math
import pdb
import doctest
from scipy.special import comb
from scipy.signal import find_peaks
from encode_k import *
from utils import *

def get_peaks(psd_array):
	"""
	Array that returns the number of peaks in pst_array not in the same freq_window or wtv
	k peaks in those time intervals
	"""
	num_peaks = k_peaks
	max_psd = 0.25 * max(psd_array)
	distance = step // 5
	ind_peaks_in_psd, _ = find_peaks(psd_array, distance=distance, height=max_psd) #indices
	ind_peaks_in_psd = np.sort(ind_peaks_in_psd)[::-1]
	
	ind_peaks_in_psd = ind_peaks_in_psd[0:num_peaks]
	length = len(ind_peaks_in_psd)

	while (length < num_peaks):
		max_psd = max_psd * 0.95
		ind_peaks_in_psd, _ = find_peaks(psd_array, height=max_psd) #indices
		ind_peaks_in_psd = np.sort(ind_peaks_in_psd)[::-1]
		ind_peaks_in_psd = ind_peaks_in_psd[0:num_peaks]
		length = len(ind_peaks_in_psd)
		print(ind_peaks_in_psd)


	# if len(ind_peaks_in_psd) == 6:
	# 	ind_peaks_in_psd = 
	result = ind_peaks_in_psd[::-1] // 5
	print(result)
	return result
	# psd_peaks_sorted = np.sort(psd_array[peaks_in_psd], axis=-1)[::-1]

	# ok so you do +5 // 10 and if you have something that is v close (for example 255 235) 
	# then you should subtract -5 from 255 since the distance thing might affect that
	#  this happens when you have chunks that are separated by 1
# def test_get_peaks():
	
# 	'''
# 	Takes in a message and plots the first 'threshold' PSDs we expect to get from hearing it.
# 	'''
# 	threshold=5
# 	# permuted_chunks = encode_peaks("abc")
# 	# permuted_chunks = encode_peaks("abd")
# 	# permuted_chunks = encode_peaks("cbd")
# 	# permuted_chunks = encode_peaks("fck")
# 	permuted_chunks = encode_peaks("ghk")
# 	# permuted_chunks = encode_peaks("xxx")
# 	# permuted_chunks = [[18, 19, 20, 21]]
# 	print(permuted_chunks)
# 	sounds = []
# 	for chunk in permuted_chunks:
# 		sounds.append(get_sound_to_play(chunk))

	
# 	for i in range(min(threshold, len(sounds))):
# 		freqs, power = np.fft.fftfreq(sounds[i].shape[-1], d=1/RATE), np.abs(np.fft.fft(sounds[i])) ** 2
# 		f, p = np.fft.fftshift(freqs), np.fft.fftshift(power)
# 		p = p[np.abs(f - middle) <= spread]
# 		f = f[np.abs(f - middle) <= spread]
# 		peak_powers = np.sort(p[find_peaks(p)[0]])[::-1]

# 	# print("ACTUAL PSD ARRAY:", p)
# 		get_peaks(p)
# 		# print([f[np.where(p == peak_powers[i])][0] for i in range(4)])
# 		plt.semilogy(f, p)
# 		plt.show()

def permutation_into_num(loc_array):
	loc_array = np.sort(loc_array, axis=-1)
	F = total_freqs
	total = 0
	for i in range(len(loc_array)):
		total += choose(F - loc_array[i] - 1, len(loc_array) - i)
	return total

"""
process_sound_from_stream is the only function that should be used by other files
every other function is just a helper for process_sound_from_stream

takes in a sound and prints out the message translated so far

this function is intended to be called in a loop each time a sound is received

The input sound_to_bits should be a function that takes in sound_data and returns the bits encoded
in the sound. "sound_data" here refers to the sound data received during the predetermined time window.
With WINDOWING=True, the assumption is that the number of encoded bits is equal to
SMALL_BLOCK_SIZE * 3. With WINDOWING=False, sound_to_bits can return any number of bits.
"""

def process_sound_from_stream(sound_data, sound_to_bits, WINDOWING=True):
	global bit_blocks_received
	global unprocessed_bits
	bit_blocks_received += sound_to_bits(sound_data)
	if(WINDOWING):
		if(len(bit_blocks_received) >= 3):
			block1 = bit_blocks_received[-3]
			block2 = bit_blocks_received[-2]
			block3 = bit_blocks_received[-1]
			unprocessed_bits += three_blocks_to_one(block1, block2, block3)
	else:
		unprocessed_bits += bit_blocks_received[-1]
	
	while(len(unprocessed_bits) >= 5):
		process_five()

	print(message_so_far)


#takes the first five unprocessed bits, translates them, removes them from unprocessed_bits
#and adds the translated letter to the end of the message so far
def process_five():
	global unprocessed_bits
	global message_so_far

	first_five = unprocessed_bits[0:5]
	rest = unprocessed_bits[5:]

	message_so_far += five_to_letter(first_five)
	unprocessed_bits = rest


#takes in five bits and returns corresponding letter
def five_to_letter(bits):
	n = int(bits, 2)
	if(n == 28):
		return '.'
	if(n == 27):
		return ' '
	char = chr(n + 96)
	if char.isalpha():
		return char
	else:
		return ''


#takes in three big blocks and returns one small block they all share
def three_blocks_to_one(block1, block2, block3):
	end_block1 = block1[SMALL_BLOCK_SIZE * 2:SMALL_BLOCK_SIZE * 3]
	mid_block2 = block2[SMALL_BLOCK_SIZE: SMALL_BLOCK_SIZE * 2]
	start_block3 = block3[0: SMALL_BLOCK_SIZE]
	
	new_small_block = ""
	for i in range(SMALL_BLOCK_SIZE):
		one_count = 0
		if(end_block1[i] == '1'):
			one_count += 1
		if(mid_block2[i] == '1'):
			one_count += 1
		if(start_block3[i] == '1'):
			one_count += 1
		
		if(one_count >= 2):
			new_small_block += '1'
		else:
			new_small_block += '0'
	
	return new_small_block

def convert_num_to_bits(chunk_num):
	"""
	returns bit str of length message_size
	"""
	bin_str = str(np.binary_repr(chunk_num))
	bin_str = '0' * (message_size - len(bin_str)) + bin_str
	return bin_str

def decode(psd_array):
	"""
	decode psd_array for 1 time step thing at a time
	return bitstr is always of length message_size
	"""
	peaks = get_peaks(psd_array)
	chunk_num = int(permutation_into_num(peaks))
	print("peaks: ", peaks)
	print('chunk_num:', chunk_num)
	bitstr = convert_num_to_bits(chunk_num)
	print('bitstr:', bitstr)
	#concatenate all these bitstrs and then convert to message
	#you can get slices of length 5 and then call f

	return bitstr

if __name__ == "__main__":
	# print(decode([]))
	test_get_peaks()

