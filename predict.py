#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from networks.network import *
from utils.preprocess_data import process_all_files, bootstrap_spectrogram, group_by_predictions 


project_dir = os.path.join(os.environ['HOME'], "workdir/MusicMap/")

net = Network()
net.load(os.path.join(project_dir, "models/balanced_40sec/9500"))

process_all_files(bootstrap_spectrogram, "music", "spectro")
preds, names = net.predict("spectro/", "results/tmp.csv")
preds, names = group_by_predictions(preds, names)

visualization.show_on_map(
	preds[:, 0], preds[:, 1], names, os.path.join(project_dir, "results/avg.png")
)
