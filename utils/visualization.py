import matplotlib.pyplot as plt
import numpy
import pandas as pd

def show_on_map(valence_array, arousal_array, annotation_array, figsize=(15, 15)):
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)
    image = plt.imread('./va_scale.jpg')
    plt.imshow(image, extent=[1, 9, 1, 9])

    plt.plot(valence_array, arousal_array, 'ro', markersize='8')
    for i, xy in enumerate(zip(valence_array, arousal_array)):
        ax.annotate(valence_array[i], xy, textcoords='data')

    plt.show()
    plt.show()