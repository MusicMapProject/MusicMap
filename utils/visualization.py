import matplotlib.pyplot as plt
import numpy
import pandas as pd
import os
import gc
plt.switch_backend('agg')

project_dir = os.environ.get("HOME") + "/workdir/MusicMap/"

def show_on_map(valence_list, arousal_list, annotations, image_name, figsize=(15, 15)):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    image = plt.imread(project_dir + 'utils/va_scale.jpg')
    plt.imshow(image, extent=[1, 9, 1, 9])

    plt.plot(valence_list, arousal_list, 'ro', markersize='8')
    for i, xy in enumerate(zip(valence_list, arousal_list)):
        ax.annotate(annotations[i], xy, textcoords='data')
    
    fig.savefig(image_name)
    plt.close(fig)
    gc.collect()