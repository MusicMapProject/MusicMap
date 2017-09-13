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


if __name__ == "__main__":
    for music in sys.argv[1:]:
        mp3_to_wav(music)
