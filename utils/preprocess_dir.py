#!/usr/bin/env python
#coding: utf-8
import os
from tqdm import tqdm

def add_postfix(dir_name, postfix):
    """
    Add postfix to all files in directory
    """

    files = os.listdir(dir_name)
    for f in tqdm(files):
        # print dir_name + f
        os.rename(dir_name + f, dir_name + f[:-4] + postfix + ".mp3")


add_postfix("../data/Deam/audio/", "D")
add_postfix("../data/1000S/clips_45seconds/", "S")
