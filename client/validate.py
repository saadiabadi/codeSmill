import sys
import tensorflow as tf 
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import tensorflow.keras as keras
import tensorflow.keras.models as krm

import json
from sklearn import metrics
import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

def read_data(filename):


    print("-- START READING DATA --")

    pkd = np.array(pd.read_csv(filename))
    print(pkd.shape)
    x = pkd[:, :16]
    y = pkd[:, 16:]
    # _, X, _, Y  = train_test_split(x, y,test_size=settings['test_size'])

    # reshaped the input data for LSTM model
    # X = X.reshape(X.shape[0], 1, X.shape[1])
    x = x.reshape(x.shape[0], 1, x.shape[1])

    return x, y

def validate(model,data):
    print("-- RUNNING VALIDATION --", flush=True)

    try:
        x_test, y_test = read_data(data)
        model_score = model.evaluate(x_test, y_test, verbose=0)
        print('Testing loss:', model_score[0])
        print('Testing accuracy:', model_score[1])
        y_pred = model.predict(x_test)
        y_pred = np.argmax(y_pred, axis=1)

        clf_report = metrics.classification_report(y_test.argmax(axis=-1),y_pred)
    except Exception as e:
        print("failed to validate the model {}".format(e),flush=True)
        raise
    
    report = { 
                "classification_report": clf_report,
                "loss": model_score[0],
                "accuracy": model_score[1]
            }

    print("-- VALIDATION COMPLETE! --", flush=True)
    return report

if __name__ == '__main__':

    from fedn.utils.kerashelper import KerasHelper
    from models.csd_model import create_seed_model

    helper = KerasHelper()
    weights = helper.load_model(sys.argv[1])
    model = create_seed_model()
    model.set_weights(weights)
    report = validate(model, '../data/test.csv')

    with open(sys.argv[2], "w") as fh:
        fh.write(json.dumps(report))
