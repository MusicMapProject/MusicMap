#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

import gc
import os
import sys

from multiprocessing import Pool

import operator
from collections import Counter

sys.path.insert(0, os.getenv("HOME") + "/workdir/MusicMap/")

from utils.mp3_to_wav import convert_one_audio
from utils.wav_file_wrapper import *

MNT_HDD_PROJECT="/mnt/hdd/music_map_project/"
MNT_SSD_PROJECT="/mnt/ssd/musicmap_data/"

DATA_MP3 = os.path.join(MNT_HDD_PROJECT, "audio")
DATA_WAV = os.path.join(MNT_HDD_PROJECT, "audio_wav")

SPECTRO = os.path.join(MNT_SSD_PROJECT, "audio_spectro_vbugaevsky")

print "DATA_MP3: {}".format(DATA_MP3)
print "DATA_WAV: {}".format(DATA_WAV)
print "SPECTRO: {}".format(SPECTRO)

if not os.path.exists(DATA_WAV):
    os.mkdir(DATA_WAV)
    
if not os.path.exists(SPECTRO):
    os.mkdir(SPECTRO)
    
for (dirpath, dirnames, filenames) in os.walk(DATA_MP3):
    break

audio_ids = map(lambda x: os.path.splitext(x)[0], filenames)
len(audio_ids)

np.random.seed(8888)

"""
if len(os.listdir(DATA_WAV)) > 0:
    raise NameError("Directory is not empty!")

try:   
    pool = Pool(processes=10)
    res = pool.map_async(convert_one_audio, zip(
        map(lambda s: s+'.mp3', audio_ids),
        [DATA_MP3] * len(audio_ids),
        [DATA_WAV] * len(audio_ids)
    ))
    res.get()
finally:
    pool.terminate()
    pool.join()
"""

def bootstrap_spectros(audio_id):
    nb_secs = 40
    
    wav_file = WavFile.read(os.path.join(DATA_WAV, audio_id+'.wav'))
    for offset in range(0, len(wav_file), nb_secs):
        if offset + nb_secs < len(wav_file):
            subsample = wav_file.get_sub_track(offset, offset + nb_secs)
            save_spectrogram(subsample, os.path.join(
                SPECTRO, "{}_{:04}.png".format(audio_id, offset)
            ), size=(256, 215), kind='mel')
            
    print audio_id+".png"
        
if len(os.listdir(SPECTRO)) > 0:
    raise NameError("Directory is not empty!")

try:
    pool = Pool(processes=15)
    res = pool.map_async(bootstrap_spectros, audio_ids)
    res.wait()
finally:
    pool.terminate()
    pool.join()
