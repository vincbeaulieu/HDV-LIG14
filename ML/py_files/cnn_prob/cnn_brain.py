
from tensorflow import keras, distribute
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.models import Sequential
import matplotlib.pyplot as plt
import numpy as np
import psutil
import multiprocessing
import tensorflow as tf
import gen_brain as gb


def cnn():
    # Create strategy
    if tf.test.is_gpu_available():
        strategy = distribute.MirroredStrategy()
    else:
        strategy = tf.distribute.OneDeviceStrategy('/cpu:0')

    with strategy.scope():
        # Create a CNN model
        model = Sequential([
            Conv2D(128, (5, 5), activation='relu', input_shape=(129, 64, 1)),
            MaxPooling2D((3, 3)),
            Conv2D(64, (4, 4), activation='relu'),
            MaxPooling2D((2, 2)),
            Conv2D(32, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(16, activation='relu'),
            Dense(1, activation='linear')
        ])
        
        # Compile the model
        model.compile(optimizer='Adam',
                    loss='mse',
                    metrics=['accuracy'])

    # Return the model
    return model


if __name__ == '__main__':
    # Load the image data and y values
    X_ori = np.load(gb.save_path + 'npy/images.npy')
    y_ori = np.load(gb.save_path + 'npy/fitness.npy')

    # Create a new copy of X and y where zero values are removed
    X = X_ori[y_ori != 0]
    y = y_ori[y_ori != 0]

    # Reshape the X to have a single channel
    X = X.reshape((-1, X.shape[1], X.shape[2], 1))

    # Split the data into training, validation, and test sets
    train_X, val_X, test_X = np.split(X, [int(0.6 * len(X)), int(0.8 * len(X))])
    train_y, val_y, test_y = np.split(y, [int(0.6 * len(y)), int(0.8 * len(y))])

    # Select/Load the model
    model = cnn()
    # model = gb.load("pkl/cnn_brain.pkl")

    # Fit the model using multiprocessing
    # gb.run_multiple(gb.fit_model, model, train_X, train_y, val_X, val_y)
    gb.fit_model(model, train_X, train_y, val_X, val_y)

    # Save the trained model
    gb.save(model, "pkl/cnn_brain.pkl")

    # Evaluate the model
    test_loss, test_mae = model.evaluate(test_X, test_y)
    print('Test MAE:', test_mae)

    # Print results of predictions
    gb.predict(model, test_X, test_y)
