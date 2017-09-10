#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pydub import AudioSegment


def mp3_to_wav(path_music):
    sound = AudioSegment.from_mp3(path_music)
    sound.export(path_music[:-4] + ".wav", format="wav")
    return path_music + ".wav"


if __name__ == "__main__":
    for music in sys.argv[1:]:
        mp3_to_wav(music)
