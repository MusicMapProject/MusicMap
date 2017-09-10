#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pydub import AudioSegment


def mp3_to_wav(path_music):
    sound = AudioSegment.from_mp3(path_music)
    sound.export(path_music + ".wav", format="wav")
    return path_music + ".wav"
