#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time

sys.path.insert(0, os.getenv("HOME") + "/workdir/MusicMap/")

from utils.preprocess_data import *
from networks.network import *

MNT_HDD_PROJECT="/mnt/hdd/music_map_project/"
MNT_SSD_PROJECT="/mnt/ssd/musicmap_data/"

MODELS_DIR = os.path.join(MNT_SSD_PROJECT, "models")

def rmDir(dirname):
    files = os.listdir(dirname)
    for file_name in files:
        file_path = os.path.join(dirname, file_name)
        if os.path.isfile(file_path):
            os.unlink(file_path)

def grepPartsOfSong(filename, dirSpectro):
    spectro_name = re.search('(-?\d+_\d+)_\d+', os.path.splitext(filename)[0]).group(0)
    found = map(lambda line: re.search(spectro_name +'.png', line), os.listdir(dirSpectro))
    return map(lambda s: s.group(0), filter(lambda s: s, found))
  
def process_predict(net, data_spectro, data_predict):
    
    backup = os.listdir(data_spectro)
    if len(backup) == 0:
        return
                
    predictions, songnames = net.predict(data_spectro + '/', data_predict)
    names_, preds_ = group_by_predictions(predictions, songnames)
    saveToCsv(names_, preds_, data_predict)

    print "Predicted!"
    
'''
    arg1 - number of model
    [arg2] - [optional] name of dir with spectro
    
    predicted in "predict_[number of model]"
'''
if __name__ == "__main__":
    
    number_model = sys.argv[1]
    if len(sys.argv) > 2:
        dir_spectro = sys.argv[2]
    else:
        dir_spectro = "spectro"
    if len(sys.argv) > 3:
        raise "Wrong number of variables" 
    
    if number_model not in os.listdir(MODELS_DIR):
        raise "Model doesn't exist"
    model_path = os.path.join(MODELS_DIR, number_model)
    
    data_predict = os.path.join(MNT_SSD_PROJECT, "predict_" + number_model) 
    
    if not os.path.isdir(data_predict):
        os.mkdir(data_predict) 
        
    rmDir(data_predict)
    
    net = Network()
    net.load(model_path)
    
    data_spectro = os.path.join(MNT_SSD_PROJECT, dir_spectro)
    
    process_predict(net, data_spectro, data_predict)