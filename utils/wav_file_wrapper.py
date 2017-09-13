#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt


class WavFile:
    def __init__(self, samples, rate, scale=False):
        """
        :param samples: audio samples
        :param rate: audio rate
        :param scale: scale sample values in [-1, 1]
        """
        if len(samples.shape) == 1:
            self.samples = samples.reshape((len(samples), 1))
        elif len(samples.shape) != 2:
            raise Exception("Wrong file format!")
        else:
            self.samples = samples
        self.rate = rate

        if scale:
            nb_bits = re.findall(r"int(\d+)", str(self.samples.dtype))
            if len(nb_bits) > 0:
                nb_bits = int(nb_bits[0])
                self.samples = np.divide(self.samples, 2.0 ** nb_bits)
            else:
                raise Exception("Wrong file format!")

    @staticmethod
    def read(file_name, scale=False):
        """
        :param file_name: input file name for "*.wav"
        :param scale: scale track values in [-1, 1]
        """
        rate, samples = wav.read(file_name)
        return WavFile(samples, rate, scale)

    def write(self, file_name):
        wav.write(file_name, self.rate, self.samples)

    def __len__(self):
        """
        :return: track's length in seconds
        """
        return self.samples.shape[0] / self.rate

    def get_nb_channels(self):
        return self.samples.shape[1]

    def get_channel(self, channel):
        return self.samples[:, channel]

    def convert_seconds_to_ticks(self, secs):
        return int(secs * self.rate)

    def get_sub_track(self, start_sec=None, end_sec=None):
        """
        :param start_sec: start position in seconds. if None, treat as 0 seconds
        :param end_sec: finish position in seconds. if None, treat as end_of_track in seconds
        :return: part of track's channel, starting form start_sec and finishing end_sec
        """
        if start_sec is not None and end_sec is not None and start_sec >= end_sec:
            raise Exception("Start should be less than end")

        l_border = 0 if start_sec is None else self.convert_seconds_to_ticks(start_sec)
        r_border = self.samples.shape[0] if end_sec is None else self.convert_seconds_to_ticks(end_sec)
        return WavFile(self.samples[l_border:r_border, :], self.rate)


def split(file_name, nb_secs, dir_dst):
    """
    :param file_name: input file name
    :param nb_secs: number of seconds in each part
    """
    filename, extension = os.path.splitext(file_name)
    wav_file = WavFile.read(file_name)

    for idx, part in enumerate(xrange(0, len(wav_file), nb_secs)):
        if part + nb_secs > len(wav_file):
            break

        wav_current = wav_file.get_sub_track(part, part + nb_secs)
        wav_current.write(
            file_name="{}{}_{}{}".format(dir_dst, os.path.basename(filename), idx, extension)
        )


def time_series(ax, sample, rate, freq=0.001):
    x = np.arange(0, len(sample) / rate, freq)
    y = sample[(x * rate).astype(int)]
    ax.plot(x, y, linewidth=0.5)


def spectrogram(ax, sample, rate, window_width, overlap_pct=0.5):
    return ax.specgram(
        x=sample,
        NFFT=window_width,
        noverlap=window_width * overlap_pct,
        Fs=rate,
        cmap='jet'
    )


def save_spectrogram(wav_file, out_path):
    """
    :param sample: sample of wav file
    :param out_path: output gistorgam save in out_path
    """
    figure = plt.figure(frameon=False)
    ax = plt.Axes(figure, [0., 0., 1., 1.])
    ax.set_axis_off()
    figure.add_axes(ax)
    # spectrum, freqs, time, image = ax.specgram(
    #     x=sample[:, 0].reshape(-1), NFFT=2**6, noverlap=2**5, Fs=2, cmap='jet'
    # )
    spectrum, freqs, time, image = \
        spectrogram(ax, wav_file.get_channel(0), wav_file.rate, wav_file.rate / 64, 0.5)
    figure.savefig(out_path)
    plt.close(figure)


if __name__ == "__main__":
    pass
