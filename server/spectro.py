#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import threading

from multiprocessing import Pool

# TODO: Fix this shit with PYTHONPATH and bash script
sys.path.insert(0, os.getenv("HOME") + "/workdir/MusicMap/")

from utils.wav_file_wrapper import *
from utils.preprocess_data import *
from utils.mp3_to_wav import convert_one_audio

MNT_HDD_PROJECT="/mnt/hdd/music_map_project/"
MNT_SSD_PROJECT="/mnt/ssd/musicmap_data/"

DATA_MP3 = os.path.join(MNT_HDD_PROJECT, "data_mp3")
DATA_WAV = os.path.join(MNT_HDD_PROJECT, "data_wav")

DATA_SPECTRO = os.path.join(MNT_SSD_PROJECT, "spectro")

BASE_SPECTRO = "spectro.base"


if not os.path.isdir(DATA_MP3):
    os.mkdir(DATA_MP3)

if not os.path.isdir(DATA_WAV):
    os.mkdir(DATA_WAV)

if not os.path.isdir(DATA_SPECTRO):
    os.mkdir(DATA_SPECTRO)


def load_proccessed_audios(file_name):
    if not os.path.isfile(file_name):
        audios = []
    else:
        with open(file_name, mode='r') as f_name:
            audios = filter(lambda x: len(x) > 0, map(lambda x: x.strip(), f_name)) 
    return audios


def dump_proccessed_audios(file_name):
    with open(file_name, mode='w') as f_name:
        for a in audio_processed:
            f_name.write(a+'\n')


audio_processed = load_proccessed_audios(BASE_SPECTRO)

convert_audio_pool = []
create_spectro_pool = []


def process_new_audios():
    t = threading.currentThread()

    global convert_audio_pool
    global audio_processed

    while getattr(t, "do_run", True):
        print "Looking for new audios..."
        audio = [
            os.path.splitext(file_name)[0]
            for root, dirs, files in os.walk(DATA_MP3)
            for file_name in files
        ]
        audio = filter(lambda f: f not in audio_processed + convert_audio_pool + \
                                create_spectro_pool, audio)[:30]
        
        if len(audio) == 0:
            print "No new audios found!"
        else:
            for a in audio:
                print a + '.mp3'
            convert_audio_pool.extend(audio)
        
        time.sleep(30)
        # TODO: Think of better way to do it


def process_convert_audio_pool():
    t = threading.currentThread()

    global audio_processed
    global convert_audio_pool
    global create_spectro_pool 

    while getattr(t, "do_run", True):
        backup = convert_audio_pool[:]

        if len(backup) == 0:
            print "process_convert_audio_pool waiting..."
            time.sleep(5)
            continue
        
        # КОСТЫЛЬ!!!
        spoiled = filter(lambda f: os.path.getsize(os.path.join(DATA_MP3, f+'.mp3')) < 2048, backup)
        backup = filter(lambda f: f not in spoiled, backup)

        try:
            pool = Pool(processes=10)
            res = pool.map_async(convert_one_audio, zip(
                    map(lambda s: s+'.mp3', backup),
                    [DATA_MP3] * len(backup),
                    [DATA_WAV] * len(backup)
            ))
            res.get()
        finally:
            pool.terminate()
            pool.join()

        convert_audio_pool = filter(lambda d: d not in backup + spoiled, convert_audio_pool)
        create_spectro_pool.extend(backup)
        audio_processed.extend(spoiled)
        
        print "Convert: Done!"


def create_spectrogram((file_name, src_dir, dst_dir)):
    wav_file = WavFile.read(os.path.join(src_dir, file_name), scale=False)
    audio_id = os.path.splitext(file_name)[0]
    
    try:
        for offset, subsample in bootstrap_track(wav_file, nb_secs=40, size=5):
            save_spectrogram(subsample, os.path.join(
                dst_dir, "{}_{}.png".format(audio_id, offset)
            ), size=(256, 215))
    except NameError:
        print os.path.splitext(file_name)[0]+'.png', "ERROR OCCURED"

    print os.path.splitext(file_name)[0]+'.png'


def process_create_spectro_pool():
    t = threading.currentThread()

    global create_spectro_pool
    global audio_processed

    while getattr(t, "do_run", True):
        backup = create_spectro_pool[:]
        if len(backup) == 0:
            print "process_create_spectro_pool waiting..."
            time.sleep(5)
            continue
        
        try:
            pool = Pool(processes=10)
            res = pool.map_async(create_spectrogram, zip(
                    map(lambda s: s+'.wav', backup),
                    [DATA_WAV] * len(backup),
                    [DATA_SPECTRO] * len(backup)
            ))
            res.get()
        finally:
            pool.terminate()
            pool.join()

        create_spectro_pool = filter(lambda d: d not in backup, create_spectro_pool)
        audio_processed.extend(backup)

        print "Spectro: Done!"
        

if __name__ == "__main__":
    t0 = threading.Thread(target=process_new_audios)
    t1 = threading.Thread(target=process_convert_audio_pool)
    t2 = threading.Thread(target=process_create_spectro_pool)

    try:
        t0.start()
        t1.start()
        t2.start()

        while True:
            pass
    finally:
        t0.do_run = False
        t1.do_run = False
        t2.do_run = False

        t0.join()
        t1.join()
        t2.join()

        dump_proccessed_audios(BASE_SPECTRO)

