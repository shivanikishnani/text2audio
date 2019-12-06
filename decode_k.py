import numpy as np
import pyaudio
import math
import pdb
import doctest
from scipy.special import comb
from scipy.signal import find_peaks
from encode_k import *


def get_peaks(psd_arr, freq_array, freq_window):
	"""
	Array that returns the number of peaks in pst_array not in the same freq_window or wtv
	k peaks in those time intervals
	"""
	max_psd = 0.25 * max(psd_array)

	peaks_in_psd = find_peaks(psd_array, height=max_psd, distance=freq_window) #indices
	return peaks_in_psd
