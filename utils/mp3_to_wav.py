#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from pydub import AudioSegment


def mp3_to_wav(path_music):
    sound = AudioSegment.from_mp3(path_music)
    name = os.path.splitext(path_music)[0] + ".wav"
    sound.export(name, format="wav")
    return name


def convert_one_audio((f, dir_src, dir_dst)):
    sound = AudioSegment.from_mp3(os.path.join(dir_src, f))
    name = os.path.splitext(f)[0] + ".wav"
    print name
    sound.export(os.path.join(dir_dst, name), format="wav")
    return name


if __name__ == "__main__":
    for music in sys.argv[1:]:
        mp3_to_wav(music)
