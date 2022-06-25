from statistics import mode
import tensorflow as tf
from tensorflow.python import keras
from keras import datasets, layers, models
import matplotlib.pyplot as plt
from keras.datasets import mnist
import pandas as pd
from keras_tuner import tuners
import numpy as np
import os
from sys import argv
import re
import cv2
from sklearn.model_selection import train_test_split
import datetime


def main():
    index_file = pd.read_csv('./cnn/chinese_mnist.csv')
    labels = sorted(index_file.value.unique())

    data = []
    width = 60
    height = 60

    for dirname, _, filenames in os.walk('./cnn/data/'):
        for filename in filenames:
            # apply regular expression to find all the numbers
            comb = re.findall('[0-9]+', filename)
            comb = [int(i) for i in comb]
            if(len(comb)==3):
                # convert the image into an array and resize it
                label = labels.index(index_file[index_file.suite_id==comb[0]][index_file.sample_id==comb[1]][index_file.code==comb[2]].value.values[0])
                image_data = cv2.imread(os.path.join(dirname, filename), cv2.IMREAD_GRAYSCALE)
                resized_data = cv2.resize(image_data, (width, height))
                data.append([resized_data, label])
            else:
                print('Incompatible file format')
                break;

    X = []
    y = []

    for feature, label in data:
        X.append(feature)
        y.append(label)

    X = np.array(X).reshape(-1, width, height, 1)
    y = np.array(y)

    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=69)

    # Convert to float32.
    x_train, x_test = np.array(x_train, np.float32), np.array(x_test, np.float32)
    # Normalize images value from [0, 255] to [0, 1].
    X_train, X_test = x_train / 255., x_test / 255. #ameliore l'entraiment

    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=x_train[0].shape))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPool2D((2, 2)))
    model.add(layers.Dropout(0.25))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(15, activation='softmax'))

    early_stop = tf.keras.callbacks.EarlyStopping(patience=3, monitor='val_loss', restore_best_weights=True)
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])


    tensorboard_callback = tf.keras.callbacks.TensorBoard(histogram_freq=1)


    model.fit(X_train, y_train, batch_size=70, epochs=15, validation_split=0.15, callbacks=[early_stop])

    model.save("models/chinese-cnn")

def recognition(image):
    try:
        model = tf.keras.models.load_model('models/chinese-cnn')
    except IOError:
            exit("model hasn't been trained yet. Run `python cnn_chinese.py compile` to train it")

    predictions = model(image)
    return np.argmax(predictions)

def guess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (60, 60), interpolation=cv2.INTER_AREA)
    newimg = tf.keras.utils.normalize(resized, axis=1)
    newimg = np.array(newimg).reshape(-1, 60, 60, 1)

    return recognition(newimg)

if __name__ == '__main__':
    if len(argv) < 2:
        exit("Need at leas one command line argument")
    elif argv[1] == 'compile':
        main()
