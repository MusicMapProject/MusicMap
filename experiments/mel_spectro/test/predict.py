#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import shutil
import operator
import itertools

PROJECT_DIR = os.getenv("HOME") + "/workdir/MusicMap/"

sys.path.insert(0, PROJECT_DIR)

RESULTS="results"
SPECTRO="spectro"

if not os.path.exists(RESULTS):
    os.mkdir(RESULTS)

from networks.network import *
from utils.visualization import show_on_map
from utils.preprocess_data import process_all_files, bootstrap_spectrogram

def group_by_predictions(preds, names):
    names = map(lambda x: '_'.join(x.split('_')[:-1]), names)
    valence, arousal = preds[:, 0].tolist(), preds[:, 1].tolist()

    preds_, names_ = [], []
    for name, grouped in itertools.groupby(
            sorted(zip(valence, arousal, names), key=operator.itemgetter(2)),
            key=operator.itemgetter(2)):
        preds_.append(np.mean(map(lambda x: (x[0], x[1]), grouped), axis=0))
        names_.append(name)

    return names_, np.array(preds_)    

net = Network()

# original model

MODEL_PATH = "/mnt/ssd/musicmap_data/models/2200_1gpu_good_spectro"
net.load(MODEL_PATH)

preds, names = net.predict(SPECTRO + '/', os.path.join(RESULTS, "{}.csv".format("original")))
names, preds = group_by_predictions(preds, names)
show_on_map(preds[:, 0], preds[:, 1], names, os.path.join(RESULTS, "{}.png".format("original")))

# working model

MODEL_PATH = os.path.join(PROJECT_DIR, "models/exp_mel_spectro/saved_models/1600")
net.load(MODEL_PATH)

preds, names = net.predict(SPECTRO + "_new" + '/', os.path.join(RESULTS, "{}.csv".format("working")))
names, preds = group_by_predictions(preds, names)
show_on_map(preds[:, 0], preds[:, 1], names, os.path.join(RESULTS, "{}.png".format("working")))
