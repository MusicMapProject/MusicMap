#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import shutil
import operator

sys.path.insert(0, os.getenv("HOME") + "/workdir/MusicMap/")

RESULTS="results"
SPECTRO="spectro"

if not os.path.exists(RESULTS):
    os.mkdir(RESULTS)

from networks.network import *
from utils.visualization import show_on_map
from utils.preprocess_data import process_all_files, bootstrap_spectrogram, group_by_predictions

net = Network()
# net.load("/mnt/ssd/musicmap_data/models/2200_1gpu_good_spectro")
net.load(os.getenv("HOME") + "/workdir/MusicMap/experiments/one_second_shift/models/200_30sec_1gpu_noshift")

for root, dirs_list, files_list in os.walk(SPECTRO):
    for dir_spectros in dirs_list:
        track_name = dir_spectros
        dir_spectros = os.path.join(root, dir_spectros) + '/'
        print dir_spectros
        
        preds, names = net.predict(dir_spectros, os.path.join(RESULTS, "{}.csv".format(track_name)))
        preds = np.asarray([x for x, _ in sorted(zip(preds, names), key=operator.itemgetter(1))])
        names = sorted(names)

        show_on_map(preds[:, 0], preds[:, 1], names, os.path.join(RESULTS, "{}.png".format(track_name)))

        print track_name
