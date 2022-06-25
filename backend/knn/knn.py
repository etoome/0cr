import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from tensorflow.keras.datasets import mnist  # Import TensorFlow's class for reading the MNIST dataset
from keras.preprocessing.image import load_img, img_to_array, smart_resize
import warnings
from collections import defaultdict
import numpy as np

def euclidean_distance(img_a, img_b):
    """
    :param img_a: numpy array representing an image as a vector
    :param img_b: numpy array representing an image as a vector
    :return: numpy.float64 representing the Euclidean distance between the images
    """
    return np.linalg.norm(img_a - img_b)  # The Euclidean distance is defined as the norm of the difference between the vectors


def find_most_frequent_element(list_int):
    """
    :param list_int: list of integers
    :return: the majority element of the list as classed by frequency of apparition
    """
    counter = defaultdict(int)  # Creates a dictionary of integers
    for element in list_int:
        counter[element] += 1
        # Each entry of the dictionary will contain the frequency of apparition of its key in the list
    majority_count = max(counter.values())
    for key, value in counter.items():
        if value == majority_count:
            return key


def predict_using_KNN(K, image, sample_images, sample_labels):
    """
    :param K: integer representing the number of neighbors considered to be in the vicinity of the image
    :param image: numpy array representing an image
    :param sample_images: list of numpy arrays representing images whose labels are known
    :param sample_labels: list of labels corresponding to the elements in sample_images
    :return: the label most likely to correspond to the image calculated using the K-Nearest-Neighbors algorithm
    """
    # Creation of a list of tuples containing the Euclidean distance of image to every element of sample_images and
    # the element's label
    list_of_distances = [(euclidean_distance(image, sample_image), sample_label)
                 for (sample_image, sample_label) in zip(sample_images, sample_labels)]
    # Sort list by distances (ascending)
    sorted_list_of_distances = sorted(list_of_distances, key=lambda tup: tup[0])
    # Extract only the K nearest labels
    k_nearest_labels = [label for (_, label) in sorted_list_of_distances[:K]]
    return find_most_frequent_element(k_nearest_labels)


def test_accuracy(K, test_images, test_labels, sample_images, sample_labels):
    nb_of_iterations = 0
    number_of_correct_guesses = 0
    for test_image in test_images:
        prediction = predict_using_KNN(K, test_image, sample_images, sample_labels)
        if prediction == test_labels[nb_of_iterations]:
            # If prediction was correct, increment number of correct guesses
            number_of_correct_guesses += 1
        accuracy = (number_of_correct_guesses / (nb_of_iterations + 1)) * 100
        print('test image[' + str(nb_of_iterations) + ']', '\tprediction:', prediction, '\treal label:', test_labels[nb_of_iterations], '\taccuracy:', str(round(accuracy, 2)) + '%')
        nb_of_iterations += 1

def guess_image(imagepath):
    """
    Will open an image, convert it to a numpy array, resize it and then predict what number it could be
    :param imagepath: path where the image can be found
    :return: number
    """
    img = load_img(imagepath, color_mode="grayscale", target_size=(28,28))
    img_numpy_array = img_to_array(img)

    (sample_images, sample_labels), (_, _) = get_sampe_tests()
    return predict_using_KNN(10, img_numpy_array, sample_images, sample_labels)


def get_sampe_tests():
    current_dir = os.getcwd()
    return mnist.load_data(path=current_dir + '/mnist.npz')

def main():
    # Load mnist database:
    current_dir = os.getcwd()
    (sample_images, sample_labels), (test_images, test_labels) = mnist.load_data(path=current_dir + '/mnist.npz')
    test_accuracy(10, test_images, test_labels, sample_images, sample_labels)

if __name__ == '__main__':
    main()
