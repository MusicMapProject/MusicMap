# -*- coding: utf-8 -*-

import logging

from tqdm import tqdm
import torch.optim as optim
from data_loader import SpectrogramDataset
import torch
import torchvision
import torchvision.transforms as transforms

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import os
import torchvision.models as models

#TODO change saving

if __name__ == '__main__':
    import os, sys

    network_dir = os.path.dirname(os.path.join(os.getcwd(), __file__))
    sys.path.append(os.path.normpath(os.path.join(network_dir, '..')))
    from utils import visualization
    from utils.preprocess_data import preprocess_dir
else:
    from utils import visualization

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

# logging.basicConfig(filename='./train.log', filemode='w', level=logging.INFO)

def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))


class Net(nn.Module):
    def __init__(self, pretrained_model):
        super(Net, self).__init__()
        self.pretrained_model = pretrained_model
        self.last_layer = torch.nn.Linear(1000, 2)

    def forward(self, x):
        return self.last_layer(self.pretrained_model(x))

    
ssd_path = "/mnt/ssd/musicmap_data/"
project_dir = os.environ.get("HOME") + "/workdir/MusicMap/"


class Network:
    def __init__(self):
        self.net = None
        self.models_dir = project_dir + "models/"
        print self.models_dir

    def load(self, model_filename):
        self.net = torch.load(model_filename)

    def predict(self, img_dir, dst_path):
        
        if not self.net:
            raise Exception("Load or train model before predict, bro")
        else:
            test_set = SpectrogramDataset(
                csv_path=None,
                img_path=img_dir,
                transform=transform,
                train=False
            )

            test_loader = torch.utils.data.DataLoader(test_set, batch_size=200,
                                                       shuffle=False, num_workers=16)

            predictions = None
            for inputs in test_loader:
                inputs = Variable(inputs.cuda())
                outputs = self.net(inputs)
                if predictions is not None:
                    predictions = np.concatenate([predictions, outputs.data.cpu().numpy()], axis=0)
                else:
                    predictions = outputs.data.cpu().numpy()

            songnames = test_set.get_songnames()


            return predictions, songnames


    def train(self, 
              train_csv="10sec/spectrs_10sec_labels_train.csv",
              validate_csv="10sec/spectrs_10sec_labels_val.csv",
              spectrs_dir="10sec/spectrs_10sec_new/",
              nb_epochs=6, verbose_step=200, save_step=80, visualize_step=20,
              model_name="10sec"):
        print "START TRAIN"
        
        model_path = self.models_dir + model_name +'/'
        saved_models = model_path + "saved_models/"
        train_pics = model_path + "train_pic/"
        
        if not os.path.isdir(model_path):
            os.mkdir(model_path)

        if not os.path.isdir(saved_models):
            os.mkdir(saved_models)

        if not os.path.isdir(train_pics):
            os.mkdir(train_pics)
        
        logging.basicConfig(filename=model_path + "train.log", filemode='w', level=logging.INFO)

        train_set = SpectrogramDataset(
            csv_path=ssd_path + train_csv,
            img_path=ssd_path + spectrs_dir,
            transform=transform
        )

        valid_set = SpectrogramDataset(
            csv_path=ssd_path + validate_csv,
            img_path=ssd_path + spectrs_dir,
            transform=transform
        )

        train_loader = torch.utils.data.DataLoader(train_set, batch_size=200,
                                                   shuffle=True, num_workers=16)

        valid_loader = torch.utils.data.DataLoader(valid_set, batch_size=200,
                                                   shuffle=False, num_workers=16)

        self.net = Net(models.resnet18())
        # self.net = torch.nn.DataParallel(Net(), device_ids=[2, 3])
        self.net.cuda()

        criterion = nn.MSELoss()
        optimizer = optim.SGD(self.net.parameters(), lr=0.001, momentum=0.9)

        for epoch in range(nb_epochs):
            # train step
            current_loss = 0.0
            for i, (inputs, labels) in enumerate(train_loader, 0):
                inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
                optimizer.zero_grad()
                outputs = self.net(inputs)

                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                current_loss += loss.data[0]

                if (i + 1) % verbose_step == 0:
                    logging.info(
                        "train; epoch = {:d}; batch_num = {:d}; loss = {:.3f}".format(
                            epoch + 1, i + 1, current_loss / verbose_step
                        ))
                    current_loss = 0.0

            # valid step
            mse_score, nb_batches = 0, 0
            for (inputs, labels) in valid_loader:
                inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
                outputs = self.net(inputs)
                mse_score += criterion(outputs, labels).data
                nb_batches += 1
            mse_score /= float(nb_batches)

            #save step
            if epoch % save_step == 0:
                torch.save(self.net, 
                           saved_models + str(epoch))

            if epoch % visualize_step == 0:
                for (inputs, labels) in valid_loader:
                    inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
                    outputs = self.net(inputs)
                    outputs = outputs.data.cpu().numpy()
                    names = valid_set.get_songnames(range(0,outputs.shape[0],4))
                    print outputs[:10]
                    print "labels", labels[:10]
                    visualization.show_on_map(
                        outputs[0::4,0], outputs[0::4,1], names, 
                        train_pics + str(epoch)
                    )
                    break

            logging.info("valid; epoch = {:d}; loss = {:.3f}".format(epoch + 1, mse_score[0]))

            print "\repochs passed: {}".format(epoch+1)

        print 'Finished Training'


if __name__ == "__main__":
    pass
    # print torch.cuda.is_available()
    # net = Network()
    # # net.train(nb_epochs=10000000, verbose_step=50)
    # net.load("../models/balanced_40sec_new/saved_models/0")
    # preprocess_dir("../data/our_audio/", nb_secs=40)
    # predictions, names = net.predict("../data/preprocess_data_our_audio/spectrs/", "./kek")
    # visualization.show_on_map(
    #                     predictions[:,0], predictions[:,1], names, "../train_pic/our_audio"
    #                 )
