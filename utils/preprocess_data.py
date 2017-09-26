#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tqdm import tqdm
from wav_file_wrapper import *
from mp3_to_wav import mp3_to_wav
from multiprocessing import Pool
import pandas as pd
import random as r
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


    #32 processes - 4 min
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
    print "WAV files cnt: ", len(files_src)

    #for split
    #8 processes - 4 min
    #1 process - 10 min
    #multiprocessing.cpu_count() == 4
    #4 processes - 5 min
    #16 processes - 3 min
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


def create_labels_for_dataset(labels_file, new_labels_file, tracks_dir):
    """
    """
    tmp_df = np.asarray(pd.read_csv(labels_file))
    song_va = {i[1]: [i[2], i[3]] for i in tmp_df}

    tracks_filename = os.listdir(tracks_dir)
    songs_parts = {}
    for track in tracks_filename:
        filename, extension = os.path.splitext(track)

        song_id = filename.split("_")[0]
        if song_id not in songs_parts:
            songs_parts[song_id] = []
        songs_parts[song_id].append(track)

    # print song_va
    #     print len(song_va)
    #     print songs_parts
    #     print len(songs_parts)

    new_labels = []
    for song in songs_parts.keys():
        if song in song_va:
            for part in songs_parts[song]:
                new_labels.append([part, song_va[song][0], song_va[song][1]])

                #     print new_labels[:10]
    new_labels = np.asarray(new_labels)
    #     print new_labels[:10]
    #     print new_labels.shape

    tmp_df = pd.DataFrame(data=new_labels, columns=["song_id", "valence", "arousal"])
    tmp_df.to_csv(new_labels_file, index=False)


def train_val_split(csv_file):
    data = pd.read_csv(csv_file).values
    validate_sample_idx = {i: 0 for i in r.sample(range(len(data)), int(len(data) * 0.1))}
    train_data = []
    validate_data = []
    for idx, sample in enumerate(data):
        if idx in validate_sample_idx:
            validate_data.append(sample)
        else:
            train_data.append(sample)

    filename, ext = os.path.splitext(csv_file)
    tmp_df = pd.DataFrame(data=train_data, columns=["song_filename", "valence", "arousal"])
    tmp_df.to_csv(filename + "_train" + ext, index=False)

    tmp_df = pd.DataFrame(data=validate_data, columns=["song_filename", "valence", "arousal"])
    tmp_df.to_csv(filename + "_val" + ext, index=False)

def preprocess_dir(dir_path, nb_secs=10):
    dir_name, path = dir_path.split("/")[-1],  "/".join(dir_path.split("/")[:-1])
    parts_dir = path + "/" + dir_name +"_parts"
    spectrs_dir =  path + "/" + dir_name + "_spectrs"
    process_all_files(split_one_audio, dir_path, parts_dir)
    process_all_files(create_one_spectrogram, parts_dir, spectrs_dir)


if __name__ == "__main__":
    # add_postfix("../data/Deam/audio/", "D")
    # add_postfix("../data/1000S/clips_45seconds/", "S")
    # add_postfix("../data/test/", "R")
    # process_all_files(split_one_audio, "../data/audio/", "../data/audio_parts_15sec/", 15)
    process_all_files(create_one_spectrogram, "../data/audio_parts_10sec/", "../data/spectrs_10sec_new/")
    # wav_file = WavFile.read("../data/audio_parts_10sec/5S_1.wav")
    # save_spectrogram(wav_file, "trololo.png", size=(256, 215))