#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import threading

from itertools import product
from shutil import copyfile

from multiprocessing import Pool

# TODO: Fix this shit with PYTHONPATH and bash script
sys.path.insert(0, os.getenv("HOME") + "/workdir/MusicMap/")

from utils.preprocess_data import *
from networks.network import *
from utils.sort_predicts import get_sorted_predict

MNT_HDD_PROJECT="/mnt/hdd/music_map_project/"
MNT_SSD_PROJECT="/mnt/ssd/musicmap_data/"

# /mnt/ssd/musicmap_data/spe
# ctro_selected_data_expand_dataset/
MODELS_DIR = os.path.join(MNT_SSD_PROJECT, "models")

DATA_SPECTRO = os.path.join(MNT_SSD_PROJECT, "/mnt/ssd/musicmap_data/spectro/")
DATA_PREDICT = os.path.join(MNT_SSD_PROJECT, "predict")

DATA_SPECTRO_WORKING = os.path.join(MNT_SSD_PROJECT, "spectro_working_tmp")

predicted_files = []

def rmDir(dirname):
    files = os.listdir(dirname)
    for file_name in files:
        file_path = os.path.join(dirname, file_name)
        if os.path.isfile(file_path):
            os.unlink(file_path)
        
def grepPartsOfSong(filename):
    spectro_name = re.findall('(-?\d+_\d+)_\d+', os.path.splitext(filename)[0])[0]
    
    found = []
    for line in os.listdir(DATA_SPECTRO):
        if spectro_name in line:
            found.append(line.strip())
            
    #found = map(lambda line: re.search(spectro_name +'.png', line), os.listdir(DATA_SPECTRO))
    #result = map(lambda s: s.group(0), filter(lambda s: s, found))
    return found
  
def process_predict(net):
    t = threading.currentThread()
    
    global predicted_files
    
    while getattr(t, "do_run", True):

        toPredict = []
        for filename in os.listdir(DATA_SPECTRO):
            song_name = re.findall('(-?\d+_\d+)_\d+', os.path.splitext(filename)[0])[0]
            if song_name not in predicted_files:
                parts = grepPartsOfSong(filename)
                if len(parts) < 5:
                    continue
                    
                for part in parts:
                    copyfile(os.path.join(DATA_SPECTRO, part), \
                             os.path.join(DATA_SPECTRO_WORKING, part))
                    toPredict.append(part)
                    
                predicted_files.append(song_name)
                   
        if len(toPredict) == 0:
            print "process_create_predict_pool waiting..."
            time.sleep(5)
            continue
         
        predictions, songnames = net.predict(DATA_SPECTRO_WORKING + '/', DATA_PREDICT)
        names_, preds_ = group_by_predictions(predictions, songnames)
        saveToCsv(names_, preds_, DATA_PREDICT)
        
        get_sorted_predict(DATA_PREDICT)
        
        
        # clear DATA_SPECTRO_WORKING
        rmDir(DATA_SPECTRO_WORKING)
        
        files = os.listdir(DATA_SPECTRO_WORKING)
        for file_name in files:
            file_path = os.path.join(DATA_SPECTRO_WORKING, file_name)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        '''
        
        
        backup = sorted(os.listdir(DATA_SPECTRO))
        step = 30
        cnt = len(backup)
        print cnt
        for load_to in range(step, cnt + 1, step):
            print load_to
            rmDir(DATA_SPECTRO_WORKING)
                    
            for file_name in backup[load_to - step : load_to]:
                print file_name
                for part in grepPartsOfSong(file_name):
                    #print part
                    copyfile(os.path.join(DATA_SPECTRO, part), \
                              os.path.join(DATA_SPECTRO_WORKING, part))
                
            predictions, songnames = net.predict(DATA_SPECTRO_WORKING + '/', DATA_PREDICT)
            names_, preds_ = group_by_predictions(predictions, songnames)
            saveToCsv(names_, preds_, DATA_PREDICT)
        '''

        print "Predicted!"
    

if __name__ == "__main__":
    
    number_model = sys.argv[1]
    
    if len(sys.argv) > 2:
        dir_spectro = sys.argv[2]
    else:
        dir_spectro = "spectro"
    """
    if len(sys.argv) > 2:
        raise "Wrong number of variables" 
    """
    
    if number_model not in os.listdir(MODELS_DIR):
        raise "Model doesn't exist"
    model_path = os.path.join(MODELS_DIR, number_model)
    
    net = Network()
    net.load(model_path)
    
    if not os.path.isdir(DATA_PREDICT):
        os.mkdir(DATA_PREDICT)
        
    rmDir(DATA_PREDICT)

    if not os.path.isdir(DATA_SPECTRO_WORKING):
        os.mkdir(DATA_SPECTRO_WORKING)
    
    #data_spectro = os.path.join(MNT_SSD_PROJECT, dir_spectro)
    
    t3 = threading.Thread(target=process_predict(net))

    try:
        t3.start()

        while True:
            pass
    finally:
        t3.do_run = False

        t3.join()
