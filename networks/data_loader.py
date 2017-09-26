from torch.utils.data import Dataset
import torch
import pandas as pd
from PIL import Image
import os
import numpy as np

class SpectrogramDataset(Dataset):
    """Dataset wrapping images and target labels.

    Arguments:
        A CSV file path
        Path to image folder
        Extension of images
        PIL transforms
        is train dataset
    """

    def __init__(self, img_path, csv_path=None, transform=None, train=True):
        self.img_path = img_path
        self.transform = transform
        self.train = train

        if train:
            self.df = pd.read_csv(csv_path, dtype={"valence":float, "arousal":float})
            self.y_train = self.df[['valence', 'arousal']].values
            self.X_train = self.df['song_filename'].values
        else:
            self.X_train = np.asarray(os.listdir(img_path))


    def __getitem__(self, index):
        img = Image.open(self.img_path + self.X_train[index])
        img = img.convert('RGB')
        if self.transform is not None:
            img = self.transform(img)

        if self.train:
            label = torch.from_numpy(self.y_train[index]).float()
            return img, label
        else:
            return img

    def __len__(self):
        return len(self.X_train)

    def get_songnames(self, idxs=None):
        if idxs:
            return self.X_train.values[idxs]
        else:
            return self.X_train
        


# dataset = SpectrogramDataset("../data/labels/spectrs_10sec_labels.csv", "../data/spectrs_10sec_new/")
# print dataset[10]