#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tqdm import tqdm
from wav_file_wrapper import split
from mp3_to_wav import mp3_to_wav
import sys


def add_postfix(dir_name, postfix):
    """
    Add postfix to all files in directory
    """

    files = os.listdir(dir_name)
    for f in tqdm(files):
        filename, extension = os.path.splitext(f)
        print dir_name + filename
        os.rename(dir_name + filename + extension, dir_name + filename + postfix + extension)

def split_all_audio(dir_src, dir_dst, nb_secs=10):
    """
    Split each audio in dir_name_src to parts nb_seconds long
    and save in dir_name_dst

    :param dir_src: source directory name
    :param dir_dst: destination directory name
    :param part_time: number of seconds in each part
    """
    if not os.path.isdir(dir_src):
        raise Exception("Source directory doesn't exist or not a directory")
    if not os.path.isdir(dir_dst):
        os.makedirs(dir_dst)

    files_src = os.listdir(dir_src)
    for f in tqdm(files_src):
        filename, extension = os.path.splitext(f)
        mp3_to_wav(dir_src + filename + extension)
        new_extension = '.wav'
        split(dir_src + filename + new_extension, nb_secs, dir_dst)
        os.remove(dir_src + filename + new_extension)


if __name__ == "__main__":
    # add_postfix("../data/Deam/audio/", "D")
    # add_postfix("../data/1000S/clips_45seconds/", "S")
    # add_postfix("../data/test/", "R")
    split_all_audio("../data/audio/", "../data/audio_parts/", 10)

