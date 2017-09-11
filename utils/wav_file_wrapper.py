#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import numpy as np
import scipy.io.wavfile as wav


class WavFile:
    def __init__(self, file_name, scale=False):
        r"""
        :param file_name: Input file name for "*.wav"

        :param scale: Scale track values in [-1, 1]
        """
        self.file_name = file_name
        self.rate, self.samples = wav.read(file_name)

        if len(self.samples.shape) == 1:
            self.samples = self.samples.reshape((len(self.samples), 1))
        elif len(self.samples.shape) != 2:
            raise Exception("Wrong file format!")

        if scale:
            nb_bits = re.findall(r"int(\d+)", str(self.samples.dtype))
            if len(nb_bits) > 0:
                nb_bits = int(nb_bits[0])
                self.samples = np.divide(self.samples, 2.0 ** nb_bits)
            else:
                raise Exception("Wrong file format!")

    def __len__(self):
        r"""
        :return: track's length in seconds
        """
        return self.samples.shape[0] / self.rate

    def get_channels(self):
        r"""
        Number of channels in track. Usually equals 2 (left and right ears).

        :return: nb_channels
        """
        return self.samples.shape[1]

    def convert_seconds_to_ticks(self, secs):
        return secs * self.rate

    def get_sub_track(self, start_sec=None, end_sec=None, channel=0):
        r"""
        :param start_sec: start position in seconds. if None, treat as 0 seconds

        :param end_sec: finish position in seconds. if None, treat as end_of_track in seconds

        :param channel: channel (usually 0 or 1)

        :return: part of track's channel, starting form start_sec and finishing end_sec
        """
        if start_sec is not None and end_sec is not None and start_sec >= end_sec:
            raise Exception("Start should be less than end")

        l_border = 0 if start_sec is None else self.convert_seconds_to_ticks(start_sec)
        r_border = self.samples.shape[0] if end_sec is None else self.convert_seconds_to_ticks(end_sec)
        return self.samples[l_border:r_border, channel]

    def split(self, nb_secs):
        """
        :param nb_secs: number of seconds in each part
        """
        print self.get_channels()
        _, extension = os.path.splitext(self.file_name)
        extension_len = len(extension)

        for idx, part in enumerate(xrange(0, len(self), nb_secs)):
            l_border = self.convert_seconds_to_ticks(part)
            if part + nb_secs > len(self):
                break
            r_border = self.convert_seconds_to_ticks(min(part + nb_secs, len(self)))
            wav.write(
                filename=self.file_name[:-extension_len] + "_" + str(idx) + self.file_name[-extension_len:],
                rate=self.rate,
                data=self.samples[l_border:r_border]
            )
            print idx
            print self.samples[l_border:r_border].shape


if __name__ == "__main__":
    pass
