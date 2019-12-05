# Experimental file to figure out the f/P relationship

import numpy as np
from matplotlib import pyplot as plt

freqs = [100, 500, 1000]
time = 1
RATE = 44100
times = np.linspace(0, 1, num=int(RATE * time), endpoint=True)

fts = [np.fft.fft(np.sin(2 * np.pi * f * times)) for f in freqs]
freqs_x = np.fft.fftfreq(len(times), d=1/RATE)

for i in range(len(freqs)):
    plt.plot(freqs_x, np.abs(fts[i])**2, label=freqs[i])

plt.legend()
plt.show()