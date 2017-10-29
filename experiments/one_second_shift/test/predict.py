#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import shutil

sys.path.insert(0, os.getenv("HOME") + "/workdir/MusicMap/")

RESULTS="results"
SPECTRO="spectro"

if not os.path.exists(RESULTS):
    os.mkdir(RESULTS)

from networks.network import *
from utils.visualization import show_on_map
from utils.preprocess_data import process_all_files, bootstrap_spectrogram, group_by_predictions

net = Network()
net.load("/mnt/ssd/musicmap_data/models/2200_1gpu_good_spectro")

for root, dirs_list, files_list in os.walk(SPECTRO):
    for dir_spectros in dirs_list:
        track_name = dir_spectros
        dir_spectros = os.path.join(root, dir_spectros) + '/'
        print dir_spectros
        
        preds, names = net.predict(dir_spectros, os.path.join(RESULTS, "{}.csv".format(track_name)))

        show_on_map(preds[:, 0], preds[:, 1], names, os.path.join(RESULTS, "{}.png".format(track_name)))

        print track_name
