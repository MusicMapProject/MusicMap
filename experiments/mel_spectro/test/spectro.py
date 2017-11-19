#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import numpy as np

import sys
sys.path.insert(0, os.getenv("HOME") + "/workdir/MusicMap/")

from multiprocessing import Pool

from utils.wav_file_wrapper import *
from utils.mp3_to_wav import *

DATA_MP3 = "data_mp3"
DATA_WAV = "data_wav"
SPECTRO = "spectro"

if not os.path.exists(DATA_WAV):
    os.mkdir(DATA_WAV)

if not os.path.exists(SPECTRO):
    os.mkdir(SPECTRO)

def save_spectro_common((offset, subsample)):
    global track_name

    save_spectrogram(subsample, os.path.join(
        SPECTRO, "{}_{:04}.png".format(track_name, offset)
    ), size=(256, 215), kind='common')
    
def save_spectro_mel((offset, subsample)):
    global track_name

    save_spectrogram(subsample, os.path.join(
        SPECTRO + "_new", "{}_{:04}.png".format(track_name, offset)
    ), size=(256, 215), kind='mel')

np.random.seed(8888)

for root, dirs_list, files_list in os.walk(DATA_MP3):
    for file_name in files_list:
        if not file_name.endswith(".mp3"):
            continue

        track_name, _ = os.path.splitext(file_name)
        print track_name

        file_name = os.path.join(DATA_WAV, convert_one_audio((file_name, DATA_MP3, DATA_WAV)))
        wav_file = WavFile.read(file_name, scale=False)

        pool = Pool(processes=5)
        args = bootstrap_track(wav_file, nb_secs=40, size=5)
        res = pool.map_async(save_spectro_common, args)
        res.wait()
        res = pool.map_async(save_spectro_mel, args)
        res.wait()
        pool.close()
        pool.join()
