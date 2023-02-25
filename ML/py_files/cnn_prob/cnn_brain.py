
from tensorflow import keras
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.models import Sequential
from keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np

save_path = "ML/py_files/cnn_prob/"


def cnn():
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
    model.compile(optimizer='adagrad',
                loss='poisson',
                metrics=['accuracy'])
                    
    # Return the model
    return model


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
    history = model.fit(train_X, train_y, epochs=10, validation_data=(val_X, val_y))  # batch_size=32

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
