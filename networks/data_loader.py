from torch.utils.data import Dataset
import torch
import pandas as pd
from PIL import Image

class SpectrogramDataset(Dataset):
    """Dataset wrapping images and target labels.

    Arguments:
        A CSV file path
        Path to image folder
        Extension of images
        PIL transforms
    """

    def __init__(self, csv_path, img_path, transform=None):
        tmp_df = pd.read_csv(csv_path, dtype={"valence":float, "arousal":float})

        self.img_path = img_path
        self.transform = transform

        self.X_train = tmp_df['song_filename'].values
        self.y_train = tmp_df[['valence', 'arousal']].values

    def __getitem__(self, index):
        img = Image.open(self.img_path + self.X_train[index])
        img = img.convert('RGB')
        if self.transform is not None:
            img = self.transform(img)

        label = torch.from_numpy(self.y_train[index]).float()
        return img, label

    def __len__(self):
        return len(self.X_train)


# dataset = SpectrogramDataset("../data/labels/spectrs_10sec_labels.csv", "../data/spectrs_10sec_new/")
# print dataset[10]