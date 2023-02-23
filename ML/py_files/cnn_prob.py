import concurrent.futures
from multiprocessing import cpu_count
import numpy as np
import pandas as pd
import toolbox

from tensorflow import keras
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.models import Sequential
from keras.optimizers import Adam

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from Lib14.data_properties import HDV_LIG14

filepath_prob = "Datasets/HDV/prob/"


# Output the data onto a ".csv" file
def check_results(data):
    print(data)
    toolbox.dataset_to_csv('ML/py_files/test/matrix.csv', data)
    exit()


# Extract and reformat the ".prob" data
def reformat(filename):
    # Extract data from ".prob" file
    image = np.loadtxt(filename, delimiter="\t")

    # Get matrix indexes of upper triangular part with offset of 2
    indexes = np.triu_indices(130, 2)

    # Reshape the image into a compact format (129 x 64)
    image = np.reshape(image[indexes], (128 + 1, 64))

    # Return the reformatted matrix
    return image


def get_dataframe():
    # Get lenght of the dataset
    len_sequences = HDV_LIG14.seq_amount

    # Initialise dataset
    dataset = [None for i in range(len_sequences)]

    for index in range(len_sequences):
        # Go through all the ".prob" files
        filename = filepath_prob + "SEQUENCE_" + str(index) + ".prob"

        # Extract and reformat the data
        img_data = reformat(filename)

        # Populates the dataset
        dataset[index] = img_data

    # Return a dataframe of the dataset
    return np.array(dataset)


# Get the data
hdv_fit = HDV_LIG14.hdv_fitness
data = get_dataframe()

# Reshape the data to (num_instances, 129, 64, 1)
data = data.reshape(data.shape[0], 129, 64, 1)

print(data)
print(data.shape)


# Create a sequential model
model = Sequential()

# Define the architecture of the model
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(1, 129, 64)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(1, activation='linear'))

# Compile the model
model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=0.001))

# Create training and testing data
x_train, x_test, y_train, y_test = train_test_split(data, hdv_fit, test_size=3 / 5)

# Fit the model to the training data
model.fit(x_train, y_train, epochs=10)  # , batch_size=32, validation_data=(x_test, y_test))

# Evaluate prediction accuracy of the model
prediction = model.predict(x_test)

# Plot the results
plt.scatter(prediction, y_test)
plt.xticks([])
plt.yticks([])
plt.show()
