from __future__ import print_function
import sys
import tensorflow as tf

import yaml
from fedn.utils.kerashelper import KerasHelper
from models.csd_model import create_seed_model
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

from ttictoc import tic,toc
import threading
import psutil
from datetime import datetime

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

def read_data(filename):


    print("-- START READING DATA --")

    pkd = np.array(pd.read_csv(filename))
    print(pkd.shape)
    x = pkd[:, :16]
    y = pkd[:, 16:]
    _, X, _, Y  = train_test_split(x, y,test_size=0.25) #settings['test_size'])

    # reshaped the input data for LSTM model
    X = X.reshape(X.shape[0], 1, X.shape[1])
    # x = x.reshape(x.shape[0], 1, x.shape[1])

    return X, Y


def train(model,data, settings):
    """
    Helper function to train the model
    :return: model
    """
    print("-- RUNNING TRAINING --", flush=True)
    x_train, y_train = read_data(data)


    model.fit(x_train, y_train, epochs=settings['epochs'], batch_size=settings['batch_size'], verbose=True)

    print("-- TRAINING COMPLETED --", flush=True)
    return model

if __name__ == '__main__':

    with open('settings.yaml', 'r') as fh:
        try:
            settings = dict(yaml.safe_load(fh))
        except yaml.YAMLError as e:
            raise (e)

    helper = KerasHelper()
    weights = helper.load_model(sys.argv[1])
    model = create_seed_model()
    model.set_weights(weights)
    model = train(model, '../data/train.csv', settings)
    helper.save_model(model.get_weights(), sys.argv[2])


