#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.getenv("HOME") + "/workdir/MusicMap/")

from networks.network import Network

net = Network()
net.train(
        train_csv="audio_spectro_csv/train.csv",
        validate_csv="audio_spectro_csv/valid.csv", 
        spectrs_dir="audio_spectro/",
        nb_epochs=1000,
        verbose_step=3,
        model_name="balanced_30sec_1gpu_good_spectro_new_dataset"
)
