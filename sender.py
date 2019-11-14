import pyaudio
import wave
import pysine
 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
 
def record(recording_time=10, filename="file.wav"):
    '''
    Record for recording_time (int) seconds and write it to filename (str).
    For debugging only.
    '''
    audio = pyaudio.PyAudio()
    
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    print("recording...")
    frames = []
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow = False)
        frames.append(data)
    print("recording done")
    

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()
    
    waveFile = wave.open(filename, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

def encode(message):
    '''
    Encodes a message (str) according to a currently very primitive scheme.
    Returns a set of tuples (freq, duration) to be passed into 'transmit'.
    Currently all durations are 0.1 seconds even though that doesn't meet the bitrate.
    '''
    min_freq = 20
    mappings = {i: round(min_freq * pow(2, i/13), 3) for i in range(128)} # ascii, step size is a semitone
    return [(mappings[ord(c)], 0.1) for c in message]

def play(message):
    encoded = encode(message)
    for e in encoded:
        pysine.sine(*e)

if __name__ == "__main__":
    play("Hello world!")