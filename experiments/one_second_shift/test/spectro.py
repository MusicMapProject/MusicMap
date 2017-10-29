#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

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

def save_spectro((offset, subsample)):
    global track_name
    global spectro_track_name

    save_spectrogram(subsample, os.path.join( 
        spectro_track_name, "{:04}.png".format(offset)
    ), size=(256, 215))

OFFSET_START = 60

for root, dirs_list, files_list in os.walk(DATA_MP3):
    for file_name in files_list:
        if not file_name.endswith(".mp3"):
            continue

        track_name, _ = os.path.splitext(file_name)
        print track_name

        file_name = os.path.join(DATA_WAV, convert_one_audio((file_name, DATA_MP3, DATA_WAV)))
        wav_file = WavFile.read(file_name, scale=False)

        spectro_track_name = "{}/{}".format(SPECTRO, track_name)
        if os.path.exists(spectro_track_name):
            shutil.rmtree(spectro_track_name)
        os.mkdir(spectro_track_name)

        pool = Pool(processes=10)
        args = [(offset, wav_file.get_sub_track(offset, offset + 40)) for offset in range(OFFSET_START, OFFSET_START + 20)]
        res = pool.map_async(save_spectro, args)
        res.wait()
        pool.close()
        pool.join()

