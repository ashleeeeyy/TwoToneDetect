"""
Two tone detect by Ashley S. on 11/15/2021
"""
import tones
from scipy.io import wavfile
import numpy as np

# load our audio data from a wav file
sample_rate, data = wavfile.read("audio.wav")
audio = np.array(data, dtype=float)

# get the low tone and the high tone
x, y = tones.get_tones(audio, sample_rate)

# add our towns tones
tones.add_mapping(tones.Mapping("Local EMS Dispatch", 344, 1204))
tones.add_mapping(tones.Mapping("Local Fire Dispatch", 598, 1209))

# set margin of error in Hz
tones.frequency_error_range = 20

# get mapping for tones
mapp = tones.get_mapping_from_tones(x, y)

if mapp:
    print(mapp.name)
