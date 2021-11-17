"""
Two tone detect by Ashley S. on 11/15/2021
"""
import numpy as np
from scipy.fft import fft
from scipy.signal import find_peaks

class Mapping:
    def __init__(self, name, lowtone, hightone):
        self.name = name
        self.lowtone = lowtone
        self.hightone = hightone

mappings = []
# how many Hz off we can be from the pre-programmed tones to recognize a page
frequency_error_range = 20

def add_mapping(m):
    mappings.append(m)

def __find_max_peak_excluding(values, peaks, index=-1):
    maxval = 0
    maxindex = 0
    for x in np.nditer(peaks):
        i = x
        val = values[i]
        if val > maxval and i != index:
            maxval = val
            maxindex = i

    return maxindex, maxval


def get_tones(signal, sampler):
    """
    Get two most prominent tones, in order from lowest frequency to highest frequency,
    from a numpy array of raw audio
    :param signal Numpy array raw audio pcm data
    :param sampler Sample Rate of the audio in Hz
    :returns x, y
    """
    fftsignal = np.abs(fft(signal))
    n = len(fftsignal)

    fftsignal = fftsignal[:n // 2]
    peaks, _ = find_peaks(fftsignal, prominence=100, )

    first_tone_index, _ = __find_max_peak_excluding(fftsignal, peaks)
    second_tone_index, _ = __find_max_peak_excluding(fftsignal, peaks, first_tone_index)

    first_tone = first_tone_index * sampler // n
    second_tone = second_tone_index * sampler // n
    return first_tone, second_tone


def get_mapping_from_tones(low, high):
    for m in mappings:
        mapping_low = m.lowtone
        mappong_high = m.hightone

        if mapping_low + frequency_error_range >= low >= mapping_low - frequency_error_range:
            if mappong_high + frequency_error_range >= high >= mappong_high - frequency_error_range:
                return m
