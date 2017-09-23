# -*- coding: utf-8 -*-

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


def train(num_epoch = 6):
    for epoch in range(num_epoch):

        running_loss = 0.0
        for i, data in tqdm(enumerate(train_loader, 0)):
            inputs, labels = data
            # print labels
            # print inputs
            inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())

            optimizer.zero_grad()
            # print inputs
            outputs = net(inputs)
            # print outputs
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.data[0]
            if i % 200 == 199:    # print every 2000 mini-batches
                print('[%d, %5d] Train loss: %.3f' %
                      (epoch + 1, i + 1, running_loss / 2000))
                running_loss = 0.0


        print "Validation"
        mse = 0
        batch_cnt = 0
        for data in validate_loader:
            inputs, labels = data
            inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
            outputs = net(inputs)
            mse += criterion(outputs, labels).data
            batch_cnt += 1
        print "\rValidation mean MSE:", mse/float(batch_cnt)


    print('Finished Training')

if __name__ == "__main__":
    ssd_path = "/mnt/ssd/"

    trainset = SpectrogramDataset(
        csv_path=ssd_path + "musicmap_data/spectrs_10sec_labels_train.csv",
        img_path=ssd_path + "/musicmap_data/spectrs_10sec_new/",
        transform=transform
    )

    validateset = SpectrogramDataset(
        csv_path=ssd_path + "musicmap_data/spectrs_10sec_labels_val.csv",
        img_path=ssd_path + "musicmap_data/spectrs_10sec_new/",
        transform=transform
    )

    train_loader = torch.utils.data.DataLoader(trainset, batch_size=50,
                                               shuffle=True, num_workers=16)

    validate_loader = torch.utils.data.DataLoader(validateset, batch_size=50,
                                                  shuffle=False, num_workers=16)

    net = Net()

    net.cuda()
    criterion = nn.MSELoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

    torch.save(net, "../models/test_model")
    train(10)

########################################################################
# Okay, so what next?
#
# How do we run these neural networks on the GPU?
#
# Training on GPU
# ----------------
# Just like how you transfer a Tensor on to the GPU, you transfer the neural
# net onto the GPU.
# This will recursively go over all modules and convert their parameters and
# buffers to CUDA tensors:
#
# . code:: python
#
#     net.cuda()
#
#
# Remember that you will have to send the inputs and targets at every step
# to the GPU too:
#
# ::
#
#         inputs, labels = Variable(inputs.cuda()), Variable(labels.cuda())
#
# Why dont I notice MASSIVE speedup compared to CPU? Because your network
# is realllly small.
#
