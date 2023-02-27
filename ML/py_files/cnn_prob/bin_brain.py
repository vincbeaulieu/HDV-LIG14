
from tensorflow import keras, distribute
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.models import Sequential
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import sklearn.metrics

import gen_brain as gb

# Define the binary classification model
def binary_classifier():
    model = Sequential([
        Conv2D(128, (5, 5), activation='relu', input_shape=(129, 64, 1)),
        MaxPooling2D((3, 3)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Return the model
    return model


if __name__ == '__main__':
    # Load the image data and y values
    X_ori = np.load(gb.save_path + 'npy/images.npy')
    y_ori = np.load(gb.save_path + 'npy/fitness.npy')

    # Create a new copy of y where non-zero values are replaced by 1
    X = np.array(X_ori)
    y = np.where(y_ori == 0, 0, 1)

    # Reshape the X to have a single channel
    X = X.reshape((-1, X.shape[1], X.shape[2], 1))

    # Split the data into training, validation, and test sets
    train_X, val_X, test_X = np.split(X, [int(0.6 * len(X)), int(0.8 * len(X))])
    train_y, val_y, test_y = np.split(y, [int(0.6 * len(y)), int(0.8 * len(y))])

    # Select/Load the model
    model = binary_classifier()
    # model = gb.load("pkl/cnn_brain.pkl")

    # Fit the model using multiprocessing
    # gb.run_multiple(gb.fit_model, model, train_X, train_y, val_X, val_y)
    gb.fit_model(model, train_X, train_y, val_X, val_y, epochs=5)

    # Save the trained model
    gb.save(model, "pkl/bin_brain.pkl")
    
    # Evaluate the model
    test_loss, test_mae = model.evaluate(test_X, test_y)
    print('Test MAE:', test_mae)

    predictions = model.predict(test_X)

    # Print results of predictions
    sklearn.metrics.confusion_matrix(predictions, test_y)
    # gb.predict(model, test_X, test_y)
