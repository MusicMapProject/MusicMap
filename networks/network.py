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

from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F

logging.basicConfig(filename='./train.log', filemode='w', level=logging.INFO)

transform = transforms.Compose(
    [transforms.ToTensor(),
     transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])


def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))


class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv3 = nn.Conv2d(16, 32, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv4 = nn.Conv2d(32, 64, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv5 = nn.Conv2d(64, 128, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(128 * 2 * 4, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
        self.fc4 = nn.Linear(10, 2)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = self.pool(F.relu(self.conv3(x)))
        x = self.pool(F.relu(self.conv4(x)))
        x = self.pool(F.relu(self.conv5(x)))
        x = x.view(-1, 128 * 2 * 4)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x)
        return x


def train(nb_epochs=6, verbose_step=200, save_step=20):
    for epoch in range(nb_epochs):

        # train step
        current_loss = 0.0
        for i, (inputs, labels) in tqdm(enumerate(train_loader, 0)):
            inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
            optimizer.zero_grad()
            outputs = net(inputs)

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
            outputs = net(inputs)
            mse_score += criterion(outputs, labels).data
            nb_batches += 1
        mse_score /= float(nb_batches)
        
        #save step
        if epoch % save_step == 0:
            torch.save(net, "../models/test_model_epoch_" + str(epoch))
        
        logging.info("valid; epoch = {:d}; loss = {:.3f}".format(epoch + 1, mse_score[0]))

        print "\repochs passed: {}".format(epoch+1)

    print 'Finished Training'


if __name__ == "__main__":
    # print torch.cuda.is_available()
    ssd_path = "/mnt/ssd/"

    train_set = SpectrogramDataset(
        csv_path=ssd_path + "musicmap_data/spectrs_10sec_labels_train.csv",
        img_path=ssd_path + "musicmap_data/spectrs_10sec_new/",
        transform=transform
    )

    valid_set = SpectrogramDataset(
        csv_path=ssd_path + "musicmap_data/spectrs_10sec_labels_val.csv",
        img_path=ssd_path + "musicmap_data/spectrs_10sec_new/",
        transform=transform
    )

    train_loader = torch.utils.data.DataLoader(train_set, batch_size=200,
                                               shuffle=True, num_workers=16)

    valid_loader = torch.utils.data.DataLoader(valid_set, batch_size=200,
                                               shuffle=False, num_workers=16)

    # net = Net()
    net= torch.nn.DataParallel(Net(), device_ids=[0,1])
    net.cuda()
    
    criterion = nn.MSELoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.8)
    # optimizer = optim.Adadelta(net.parameters(), lr=0.01)

    train(nb_epochs=10000000, verbose_step=50)
