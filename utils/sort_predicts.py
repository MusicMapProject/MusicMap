import numpy as np
import pandas as pd
import os
from math import sqrt


def get_sorted_predict(predict_dir):
    files = os.listdir(predict_dir)
    for f in files:
        if f.strip().split("_")[-1] != "sorted":
            sort_fullid(os.path.join(predict_dir, f))

def sort_fullid(data_file):
    data = pd.read_csv(data_file)
    
    start_idx = 0
    for row_idx, row in enumerate(data['songnames'][::-1]):
#         print row_idx, row
        if row == 'songnames':
            start_idx = len(data['songnames']) - row_idx
            break
        
    songnames = data['songnames'][start_idx:].values
    dist_data = np.zeros(shape = (len(songnames),len(songnames)))

    for i_idx, i in enumerate(data[['valence', 'arousal']].values[start_idx:]):
        for j_idx, j in enumerate(data[['valence', 'arousal']].values[start_idx:]):
    #         print i, j, i_idx, j_idx
            dist_data[i_idx, j_idx] = sqrt((float(i[0]) - float(j[0]))**2 + (float(i[1])-float(j[1]))**2)

    sort_fullid = []

    for row_idx, row in enumerate(dist_data):
        ind = np.argsort(dist_data[row_idx])
        sort_fullid.append(songnames[ind])

    sort_fullid = np.asarray(sort_fullid)
    pd.DataFrame(data=sort_fullid).to_csv(data_file + "_sorted", index = False, header = None)
    
if __name__ == "__main__":
    get_sorted_predict("/mnt/ssd/musicmap_data/predict/")