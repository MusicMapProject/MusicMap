#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt


class WavFile:
    def __init__(self, file_name, scale=False):
        self.file_name = file_name
        self.rate, self.samples = wav.read(file_name)

        if scale:
            nb_bits = re.findall(r"int(\d+)", str(self.samples.dtype))
            if len(nb_bits) > 0:
                nb_bits = int(nb_bits[0])
                self.samples = np.divide(self.samples, 2.0 ** nb_bits)
            else:
                raise Exception("Wrong input format")

    def __len__(self):
        return self.samples.shape[0] / self.rate

    def get_channels(self):
        return self.samples.shape[1]

    def get_sub_track(self, start_sec=None, end_sec=None, channel=0):
        if start_sec is not None and end_sec is not None and start_sec >= end_sec:
            raise Exception("Start should be less then end")
        l_border = 0 if start_sec is None else start_sec * self.rate
        r_border = len(self) if end_sec is None else end_sec * self.rate
        return self.samples[l_border:r_border, channel]


def create_spectrogram(sample, sample_rate):
    figure = plt.figure(frameon=False)
    spectrum, freqs, time, image = plt.specgram(
        x=sample, NFFT=1024, noverlap=512, Fs=sample_rate, sides='onesided', cmap='jet'
    )
    print time.shape, freqs.shape
    return figure


wav_file = WavFile("Linkin Park_-_Numb.mp3.wav", scale=True)
print len(wav_file)

figure = create_spectrogram(wav_file.get_sub_track(start_sec=15, end_sec=25, channel=0), wav_file.rate)
figure.savefig("ocean_0.png", bbox_inches="tight")

wav_file = WavFile("ocean.wav", scale=True)
print len(wav_file)

figure = create_spectrogram(wav_file.get_sub_track(start_sec=15, end_sec=200, channel=0), wav_file.rate)
figure.savefig("ocean_1.png", bbox_inches="tight")
