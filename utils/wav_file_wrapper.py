#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gc
import re
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

import librosa
from librosa.display import specshow


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
    :param dir_dst: destination directory, where split files will be stored
    """
    filename, extension = os.path.splitext(file_name)
    wav_file = WavFile.read(file_name)

    for idx, part in enumerate(xrange(0, len(wav_file), nb_secs)):
        if part + nb_secs > len(wav_file):
            break

        wav_current = wav_file.get_sub_track(part, part + nb_secs)
        wav_current.write(
            file_name=os.path.join(dir_dst, "{}_{}{}".format(os.path.basename(filename), idx, extension))
        )


def bootstrap_track(wav_file, nb_secs, size=10):
    """
    :param wav_file: WavFile object
    :param nb_secs: length of sampled track
    :param size: times to bootstrap
    :return: list of pairs (offset, subsample)
    """
    transfer = len(wav_file) - nb_secs
    mean, std = transfer / 2.0, transfer / 8.0

    offsets = np.random.normal(loc=mean, scale=std, size=size).astype(int)
    offsets = np.clip(offsets, 0, transfer).tolist()
    return [(offset, wav_file.get_sub_track(offset, offset + nb_secs)) for offset in offsets]


def save_spectrogram(wav_file, png_image, size=(256, 256), kind='common'):
    """
    :param wav_file:  WavFile object
    :param png_image: output file *.png
    :param size: output size of image. default = 1 + wav_file.rate / 2
    :param kind: type of spectrogram: either 'common' or 'mel'
    """
    S = {'common': librosa.stft(wav_file.get_channel(0)),
         'mel': librosa.feature.melspectrogram(y=wav_file.get_channel(0), sr=wav_file.rate)}[kind]
    D = librosa.power_to_db(S, ref=np.max)

    figure = plt.figure(frameon=False, figsize=size, dpi=1)
    ax = plt.Axes(figure, [0., 0., 1., 1.])
    ax.set_axis_off()
    figure.add_axes(ax)
    specshow(D, y_axis='linear', cmap='jet')
    try:
        figure.savefig(png_image.encode("utf-8"), dpi=1)
    except:
        pass
    plt.close(figure)
    gc.collect()


if __name__ == "__main__":
    pass
