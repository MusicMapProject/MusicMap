#!/usr/bin/env python
#coding: utf-8
import os
from tqdm import tqdm
import wav_file_wrapper

def add_postfix(dir_name, postfix):
    """
    Add postfix to all files in directory
    """

    files = os.listdir(dir_name)
    for f in tqdm(files):
        # print dir_name + f
        os.rename(dir_name + f, dir_name + f[:-4] + postfix + ".mp3")

def split_audio(dir_name,  part_time):
    """
    Split each audio in directory to parts with part_time long
    :param dir_name: directory name
    :param part_time: count second in each part
    :return: splitted files in dir_name
    """
    files = os.listdir(dir_name)
    for f in tqdm(files):
        mp3_to_wav(dir_name + f)./
        x = WavFile(dir_name + f)
        x.split(part_time)


# add_postfix("../data/Deam/audio/", "D")
# add_postfix("../data/1000S/clips_45seconds/", "S")