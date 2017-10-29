#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import codecs
import numpy as np

import matplotlib.pyplot as plt

EPOCH_PATTERN = r'epoch = (\d+)'
SCORE_PATTERN = r'loss = (\d+\.?\d*)'


def extract_train_valid_scores(file_name):
    train_score, valid_score = [], []
    epochs = []

    with codecs.open(file_name, encoding='utf-8', mode='r') as f_logs:
        train_score_curr = []

        for line in f_logs:
            if "train" in line:
                score = float(re.findall(SCORE_PATTERN, line)[0])
                train_score_curr.append(score)
            if "valid" in line:
                train_score.append(np.mean(train_score_curr))
                train_score_curr = []
                score = float(re.findall(SCORE_PATTERN, line)[0])
                valid_score.append(score)
                epoch = int(re.findall(EPOCH_PATTERN, line)[0])
                epochs.append(epoch)

        return train_score, valid_score, epochs


def create_plot(file_logs, file_plot, skip_first=10, window_width=10):
    train_loss, valid_loss, epochs = extract_train_valid_scores(file_logs)
    train_loss, valid_loss, epochs = train_loss[skip_first:], valid_loss[skip_first:], epochs[skip_first:]
    train_loss = [np.mean(train_loss[i: i + window_width]) for i in range(0, len(train_loss) - window_width)]
    valid_loss = [np.mean(valid_loss[i: i + window_width]) for i in range(0, len(valid_loss) - window_width)]
    epochs = epochs[-len(train_loss):]

    plt.figure(figsize=(50, 20))
    plt.rc('axes', labelsize=50)
    plt.rc('xtick', labelsize=30)
    plt.rc('ytick', labelsize=30)
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.plot(epochs, train_loss, label='Train')
    plt.plot(epochs, valid_loss, label='Valid')
    plt.legend()

    plt.savefig(file_plot)


if __name__ == "__main__":
    create_plot("train.log", "loss.png", skip_first=10, window_width=1)
