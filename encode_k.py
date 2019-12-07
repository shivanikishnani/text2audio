import numpy as np
import pyaudio
import math
import pdb
import doctest
from utils import *
from scipy.special import comb
from matplotlib import pyplot as plt

"""
messages (str) -> (str2str) windowed messages ->  (str2str) bits -> 
(str2listofstr_) message_size chunks of bits
 -> (str_2array) an array of peaks locations corresponding to each chunk
""" 

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
		return message
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
	lst = str(np.binary_repr(char_to_ind(char) + 1))
	num_zero = "0" * (5 - len(lst))
	lst = num_zero + lst

	return lst

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

def num_into_permutation(n):
	F = total_freqs
	k = k_peaks
	return num_into_permutation_helper(n + 1, F, k)

def num_into_permutation_helper(n, F, k):
	i = k
	if(k == 0):
		return []
	while(n > choose(i, k)):
		i+=1
	base_amount = choose(i - 1, k)
	return [F - i] + [x + (F - i + 1) for x in num_into_permutation_helper(n - base_amount, i - 1, k - 1)]

def choose(n, r):
	if(r > n):
		return 0
	fact = math.factorial
	return (fact(n)) // (fact(r)*fact(n - r))

def convert_bitstr_to_num(str):
	lst = [eval(c) for c in str]
	l = message_size - 1
	num = 0
	for i, c in enumerate(lst):
		num += 2**(l - i) * c
	# lst = np.packbits(lst, bitorder='little')
	
	return num

def choose(n, r):
	if(r > n):
		return 0
	fact = math.factorial
	return (fact(n))/(fact(r)*fact(n - r))


def encode_peaks(message):
	'''
	Cleans the message, convert characters to bits, 
	Convert message to bits 
	find floor fo log_2 (k)
	'''

	window_message = window_str(clean(message), windowing=False)
	window_bits = "".join([char_to_bin(c) for c in window_message])
	print(window_bits)
	#divide it into chunks
	print('message size: ', message_size)
	pad = 0
	if len(window_bits) % message_size:
		pad = message_size - (len(window_bits) % message_size)
	window_bits = "0" * pad + window_bits
	print('padded:', window_bits)
	chunk_bits = [window_bits[i:i+message_size] for i in range(0, len(window_bits), message_size)]
	print('chunk_bits', chunk_bits)
	# chunk_bits = ["0" * (message_size - len(chunk)) + chunk for chunk in chunk_bits]
	# print('chunk_bits', chunk_bits)

	chunk_nums = [convert_bitstr_to_num(chunk) for chunk in chunk_bits]
	print('chunk_nums:', chunk_nums)
	permuted_chunks = [num_into_permutation(n) for n in chunk_nums]
	permuted_chunks = [[c + noise_cutoff for c in chunk] for chunk in permuted_chunks]
	print('permuted_chunks:', permuted_chunks)
	return permuted_chunks

def get_sound_to_play(chunk):
	'''
	Takes in a chunk from chunk_bits, and returns the sound to play.
	'''
	sound = np.zeros(int(RATE * d),)
	for peak in chunk:
		f = lowest + step * peak
		sound[pop:] += band_sine(f, step / 4)[pop:]

	return sound

if __name__ == "__main__":
	chunks = encode_peaks("abc")
	print(chunks)
	chunks = encode_peaks("abd")
	print(chunks)
	# for chunk in chunks:
	# 	plt.plot(get_sound_to_play(chunk))
	# 	plt.show()

