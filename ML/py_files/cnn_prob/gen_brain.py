
from tensorflow import keras, distribute
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.models import Sequential
import matplotlib.pyplot as plt
import numpy as np
import psutil
import multiprocessing
import tensorflow as tf
import gen_brain as gb

import os
import pickle as pk

save_path = "ML/py_files/cnn_prob/"

# Get system stats
nb_cores = psutil.cpu_count()
nb_threads = multiprocessing.cpu_count()

# Define the function to run in parallel
def fit_model(model, train_X, train_y, val_X, val_y, epochs=10):
    # with tf.device('/cpu:0'):
    model.fit(train_X, train_y, validation_data=(val_X, val_y), epochs=epochs)
    

# Run the model.fit function in parallel
def run_multiple(function, *args):
    with multiprocessing.Pool(processes=nb_cores) as pool:
        results = pool.starmap(function, [args] * nb_cores)
    return results


# Evaluate prediction accuracy of the model
def predict(model, test_X, test_y):
    # Predict on test data
    predictions = model.predict(test_X)

    # Plot the results
    plt.scatter(predictions, test_y)
    plt.xticks([])
    plt.yticks([])
    plt.show()

    # Return results
    return predictions


# Save model (file extension: ".pkl")
def save(model, name, filepath=save_path):
    os.makedirs(os.path.dirname(filepath + name), exist_ok=True)
    pk.dump(model, open(filepath + name, 'wb'))


# Load model (file extension: ".pkl")
def load(name, filepath=save_path):
    model = pk.load(open(filepath + name, 'rb'))
    return model
