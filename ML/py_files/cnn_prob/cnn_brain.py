
from tensorflow import keras, distribute
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.models import Sequential
import matplotlib.pyplot as plt
import numpy as np
import psutil
import multiprocessing

import tensorflow as tf

save_path = "ML/py_files/cnn_prob/"

# Get system stats
nb_cores = psutil.cpu_count()
nb_threads = multiprocessing.cpu_count()

def cnn():
    # Create strategy
    if tf.test.is_gpu_available():
        strategy = distribute.MirroredStrategy()
    else:
        strategy = tf.distribute.OneDeviceStrategy('/cpu:0')

    with strategy.scope():
        # Create a CNN model
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(129, 64, 1)),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(64, activation='relu'),
            Dense(1, activation='linear')
        ])
        
        # Compile the model
        model.compile(optimizer='Adam',
                    loss='mse',
                    metrics=['accuracy'])

    # Return the model
    return model


# Define the function to run in parallel
def fit_model(model, train_X, train_y, val_X, val_y, epochs=10):
    #with tf.device('/cpu:0'):
    model.fit(train_X, train_y, validation_data=(val_X, val_y), epochs=epochs)
    

if __name__ == '__main__':
    # Load the image data and y values
    X = np.load(save_path + 'images.npy')
    y = np.load(save_path + 'fitness.npy')

    # Reshape the X to have a single channel
    X = X.reshape((-1, X.shape[1], X.shape[2], 1))

    # Split the data into training, validation, and test sets
    train_X, val_X, test_X = np.split(X, [int(0.6 * len(X)), int(0.8 * len(X))])
    train_y, val_y, test_y = np.split(y, [int(0.6 * len(y)), int(0.8 * len(y))])

    # Select the model
    model = cnn()

    # Fit the model to the training data
    # history = model.fit(train_X, train_y, epochs=10, validation_data=(val_X, val_y))  # batch_size=32

    # Run the model.fit function in parallel
    with multiprocessing.Pool(processes=nb_cores) as pool:
        results = pool.starmap(fit_model, [(model, train_X, train_y, val_X, val_y)] * nb_cores)
        # [r.get() for r in results]

    # Evaluate the model
    test_loss, test_mae = model.evaluate(test_X, test_y)
    print('Test MAE:', test_mae)

    # Evaluate prediction accuracy of the model
    prediction = model.predict(test_X)

    # Plot the results
    plt.scatter(prediction, test_y)
    plt.xticks([])
    plt.yticks([])
    plt.show()
