#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tqdm import tqdm
from wav_file_wrapper import *
from mp3_to_wav import mp3_to_wav
from multiprocessing import Pool
import warnings
import numpy


def add_postfix(dir_name, postfix):
    """
    Add postfix to all files in directory

    ::
    """

    files = os.listdir(dir_name)
    for f in tqdm(files):
        filename, extension = os.path.splitext(f)
        os.rename(dir_name + filename + extension, dir_name + filename + postfix + extension)


def split_one_audio((f, dir_src, dir_dst, nb_secs)):
    """
    Split mp3 file from dir_src to parts and save to dir_dst directory

    :f: filename
    :dir_src: source directory
    :dir_dst: destination directory
    :nb_secs: number of seconds in each part
    :return:
    """
    filename, extension = os.path.splitext(f)
    mp3_to_wav(dir_src + filename + extension)
    new_extension = '.wav'
    # print "create " + dir_src + filename + new_extension
    split(dir_src + filename + new_extension, nb_secs, dir_dst)
    os.remove(dir_src + filename + new_extension)
    # print "delete " + dir_src + filename + new_extension


def create_one_spectrogram((f, dir_src, dir_dst)):
    """
    :f: wav filename
    :dir_src: source directory
    :dir_dst: destination directory
    :return:
    """
    filename, extension = os.path.splitext(f)
    wav_file = WavFile.read(dir_src + f)
    save_spectrogram(wav_file, dir_dst + filename, size=(256, 215))


def process_all_files(process_function, dir_src, dir_dst, function_param=None):
    """
    Function for process all files in directory with process function with parameter
    :param process_function: process function
    :param dir_src: source directory
    :param dir_dst: destination directory
    :param function_param: parameter for process function
    :return:
    """
    if not os.path.isdir(dir_src):
        raise Exception("Source directory doesn't exist or not a directory")
    if not os.path.isdir(dir_dst):
        os.makedirs(dir_dst)

    files_src = os.listdir(dir_src)
    print len(files_src)
    print len(set(files_src))

    #for split
    #8 processes - 4 min
    #1 process - 10 min
    #multiprocessing.cpu_count() == 4
    #4 processes - 5 min
    #16 processes - 3 min
    #32 processes - 4 min
    pool = Pool(processes=16)

    if function_param is not None:
        res = pool.map_async(
            process_function,
            zip(files_src, [dir_src] * len(files_src), [dir_dst] * len(files_src), [function_param] * len(files_src))
        )
    else:
        res = pool.map_async(
            process_function,
            zip(files_src, [dir_src] * len(files_src), [dir_dst] * len(files_src))
        )
    res.get()
    pool.close()
    pool.join()


if __name__ == "__main__":
    # add_postfix("../data/Deam/audio/", "D")
    # add_postfix("../data/1000S/clips_45seconds/", "S")
    # add_postfix("../data/test/", "R")
    #process_all_files(split_one_audio, "../data/audio/", "../data/audio_parts_10sec/", 10)
    process_all_files(create_one_spectrogram, "../data/audio_parts_10sec/", "../data/spectrs_10sec/")