import tensorflow as tf
from keras.backend import sparse_categorical_crossentropy
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, BatchNormalization, Dropout
from keras.models import save_model, Sequential
from keras import layers, models
from keras.datasets import mnist
import numpy as np
from sys import argv
import cv2

def main():
    from statistics import mode
    import tensorflow as tf
    from tensorflow.python import keras
    from keras import datasets, layers, models
    import matplotlib.pyplot as plt
    from keras.datasets import mnist
    import kerastuner
    from kerastuner import tuners
    import numpy as np

    # Prepare MNIST data.
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
    # Convert to float32.
    x_train, x_test = np.array(x_train, np.float32), np.array(x_test, np.float32)
    # Normalize images value from [0, 255] to [0, 1].
    x_train, x_test = x_train / 255., x_test / 255. #ameliore l'entraiment

    x_train = x_train.reshape(60000,28,28,1)
    x_test = x_test.reshape(10000,28,28,1)

    model = models.Sequential()
    model.add(layers.Conv2D(8, (3, 3), strides=(3,3), activation='relu', input_shape=x_train[0].shape))
    model.add(layers.Conv2D(8, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))


    model.summary()

    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    history = model.fit(x_train, y_train, batch_size=128, epochs=10, verbose=1,
                        validation_data=(x_test, y_test))


def main1():
    # Model configuration
    img_width, img_height = 28, 28
    batch_size = 128
    no_epochs = 10
    verbosity = 1

    # Load MNIST dataset
    (input_train, target_train), (input_test, target_test) = mnist.load_data()

    # Reshape data
    input_train = input_train.reshape(input_train.shape[0], img_width, img_height, 1)
    input_test = input_test.reshape(input_test.shape[0], img_width, img_height, 1)
    input_shape = (img_width, img_height, 1)

    # Cast numbers to float32
    input_train = input_train.astype('float32')
    input_test = input_test.astype('float32')

    # Scale data
    input_train = input_train / 255
    input_test = input_test / 255

    # Create the model
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(img_height, img_width, 1)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(10, activation='softmax'))

    # Compile model
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    # Fit data to model
    model.fit(input_train, target_train,
              batch_size=batch_size,
              epochs=no_epochs,
              verbose=verbosity,
              validation_data=(input_test, target_test))

    # Generate generalization metrics
    score = model.evaluate(input_test, target_test, verbose=0)
    print(f'Test loss: {score[0]} / Test accuracy: {score[1]}')

    # Save the model
    save_model(model, "models/cnn-model")

def recognition(image):
    try:
        model = tf.keras.models.load_model('models/cnn-model')
    except IOError:
        print("model hasn't been trained yet. Run `python cnn.py compile` to train it")
        raise

    predictions = model(image)
    return np.argmax(predictions)


def guess_image(image_path):
    """
    Gets a numpy array corresponding to an image as parameter and returns what letter it should be associated with
    """
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (28, 28), interpolation=cv2.INTER_AREA)
    newimg = tf.keras.utils.normalize(resized, axis=1)
    newimg = np.array(newimg).reshape(-1, 28, 28, 1)

    return recognition(newimg)


def test():
    """
    Test the model against images
    """

    for i in range(10):
        print(f"-----\nTrying to recognise {i}\n")
        guess = guess_image(f"test/{i}.png")
        if guess == i:
            print(f"{i} == {guess}")
        else:
            print(f"{i} != {guess}")


if __name__ == '__main__':
    if len(argv) < 2:
        exit("Need at leas one command line argument")
    elif argv[1] == 'compile':
        main()
    elif argv[1] == 'test':
        test()
    else:
        exit("Unknown argument")
