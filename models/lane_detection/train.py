import os
import numpy as np
import pandas as pd
import cv2
import random
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
import datetime
from keras.callbacks import ModelCheckpoint
from keras.callbacks import CSVLogger
import csv
from keras.callbacks import Callback

ROOT_DIR = os.getcwd()
DATA_DIR = os.path.join(ROOT_DIR, 'DATASET_CANNY')

def shuffle_data(dir, label):
    file = open(os.path.join(dir, label), 'r')
    file.readline()
    arr = []

    for item in file:
        arr.append(item)

    random.shuffle(arr)

    return arr

def load_data(dir, label):
    x_train = []
    y_train = []

    data = shuffle_data(dir, label)
    for row in data:
        row = row.rstrip().split(',')
        img = cv2.imread(os.path.join(dir, row[0]))
        img = cv2.resize(img, (128, 128))

        x_train.append(img)
        label_X = 0 if row[1] == "STRAIGHT" else 1 if row[1] == 'NORMAL' else 2
        y_train.append(label_X)

    return (x_train, y_train)

def build_model():
    model = Sequential()
    model.add(Conv2D(32, (3,3), padding='same', input_shape = x_train[0].shape))


    ## EN IYI MODEL
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Flatten())
    model.add(Dropout(0.25))
    model.add(Dense(num_classes, activation='softmax'))

    ## IKINCI MODEL
    # model.add(Activation('relu'))
    # model.add(Flatten())
    # model.add(Dense(num_classes, activation='softmax'))

    ## UCUNCU MODEL
    # model.add(Activation('relu'))
    # model.add(MaxPooling2D(pool_size=(2,2)))
    # model.add(MaxPooling2D(pool_size=(2,2)))
    # model.add(Flatten())
    # model.add(Dropout(0.25))
    # model.add(Dense(num_classes, activation='softmax'))



    model.summary()
    model.compile(loss=keras.losses.categorical_crossentropy, optimizer = 'adam', metrics = ['accuracy'])
    return model

class NBatchLogger(Callback):
    """
    A Logger that log average performance per `display` steps.
    """
    def __init__(self, display):
        self.step = 0
        self.display = display
        self.metric_cache = {}
        self.f = open('log.txt', 'a')

    def on_batch_end(self, batch, logs={}):
        self.step += 1
        for k in self.params['metrics']:
            if k in logs:
                self.metric_cache[k] = self.metric_cache.get(k, 0) + logs[k]
        if self.step % self.display == 0:
            metrics_log = ''
            for (k, v) in self.metric_cache.items():
                val = v / self.display
                if abs(val) > 1e-3:
                    metrics_log += ' - %s: %.4f' % (k, val)
                else:
                    metrics_log += ' - %s: %.4e' % (k, val)
            print('step: {}/{} ... {}'.format(self.step,
                                          self.params['steps'],
                                          metrics_log))
            self.f.write(metrics_log + '\n')
            self.metric_cache.clear()

if __name__ == '__main__':
    num_classes = 3

    x_train, y_train = load_data(DATA_DIR, 'temp.txt')
    x_train = np.array(x_train).astype('float32')
    #x_train = x_train.astype('float32')
    x_train /= 255
    y_train = keras.utils.to_categorical(y_train, num_classes)

    model = build_model()

    # model.load_weights("models_v3/8-22-22-52.h5")

    date = datetime.datetime.now()
    file_name = 'log/' + str(date.day) + '-' + str(date.hour) + '-' + str(date.minute) + '-' + str(date.second) + '.h5'

    checkpoint = ModelCheckpoint(file_name, monitor = 'loss',
                                            verbose=1,
                                            save_best_only = True,
                                            mode = 'auto',
                                            period = 1)

    out_batch = NBatchLogger(display=100) ## batchsize

    model.fit(x_train, np.array(y_train), callbacks = [out_batch],
                                          batch_size = 1,
                                          epochs = 1,
                                          verbose = 1,
                                          validation_split = 0.2)


