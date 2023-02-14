import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
import tensorflow as tf
import pickle as pk

from Lib14.data_properties import HDV_LIG14
import toolbox

# Defining filepaths:
filepath_flat = 'ML/raw/flat/'
filepath_encoded = 'ML/raw/encoded/'
filepath_prediction = 'ML/raw/prediction/'
filepath_saved_model = 'ML/pkl/'

filename_saved_model = 'test_model.pkl'


# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

def dim_redux():
    # Read and Load Files
    nt_flat = toolbox.csv_reader(filepath_flat + 'nt_flat.csv')
    db_flat = toolbox.csv_reader(filepath_flat + 'db_flat.csv')
    kt_flat = toolbox.csv_reader(filepath_flat + 'kt_flat.csv')
    lp_flat = toolbox.csv_reader(filepath_flat + 'lp_flat.csv')

    lst_flat = [nt_flat, db_flat, kt_flat, lp_flat]

    # Check for missing files
    if None in lst_flat:
        # Compute Dimensionality Reduction
        lines = toolbox.reader(filepath_encoded + 'nt_encoded.csv')
        nt_flat = toolbox.merge(lines, 3)
        nt_flat = toolbox.dataset_to_csv(filepath_flat + 'nt_flat.csv', nt_flat)
        # nt_size = len(nt_flat.axes[1])

        lines = toolbox.reader(filepath_encoded + 'db_encoded.csv')
        db_flat = toolbox.merge(lines, 4)
        db_flat = toolbox.dataset_to_csv(filepath_flat + 'db_flat.csv', db_flat)
        # db_size = len(db_flat.axes[1])

        lines = toolbox.reader(filepath_encoded + 'kt_encoded.csv')
        kt_flat = toolbox.merge(lines, 6)
        kt_flat = toolbox.dataset_to_csv(filepath_flat + 'kt_flat.csv', kt_flat)
        # kt_size = len(kt_flat.axes[1])

        lines = toolbox.reader(filepath_encoded + 'lp_encoded.csv')
        lp_flat = toolbox.merge(lines, 1)
        lp_flat = toolbox.dataset_to_csv(filepath_flat + 'lp_flat.csv', lp_flat)
        # lp_size = len(lp_flat.axes[1])

    else:
        # Convert to DataFrame
        nt_flat = pd.DataFrame(nt_flat)
        db_flat = pd.DataFrame(db_flat)
        kt_flat = pd.DataFrame(kt_flat)
        lp_flat = pd.DataFrame(lp_flat)

    # Then return data
    return nt_flat, db_flat, kt_flat, lp_flat


def neural_network():
    # Import desired outputs
    hdv_fit = HDV_LIG14.hdv_fitness
    hdv_del = HDV_LIG14.hdv_delta
    lig_fit = HDV_LIG14.ligase_fitness
    lig_del = HDV_LIG14.ligase_delta

    # Merge, Align, and Save Data
    hdv_flat = [hdv_fit, hdv_del, lig_fit, lig_del]
    hdv_flat = np.transpose(hdv_flat)
    hdv_flat = toolbox.dataset_to_csv(filepath_flat + 'hdv_flat.csv', hdv_flat)

    # Compute Dimensionality Reduction
    nt_flat, db_flat, kt_flat, lp_flat = dim_redux()

    dataframe = pd.concat([nt_flat, db_flat, kt_flat, lp_flat], axis=1)
    dataframe_size = len(dataframe.axes[1])
    dataframe = np.asarray(dataframe).astype(np.byte)

    hdv_flat = np.asarray(hdv_flat).astype('float32')

    # ANN for NT Data
    x_train, x_test, y_train, y_test = train_test_split(dataframe, hdv_flat, test_size=3/5)
    # NOTE: 10-fold cross-validation may be implemented

    # Artificial Neural Network
    model = tf.keras.models.Sequential()

    # Verify if model exist, create a model if it doesn't
    if os.path.exists(filepath_saved_model + filename_saved_model):
        # Load model if it exists
        model = load(filepath_saved_model + filename_saved_model)
        weights = model.get_weights()
        model.compile(optimizer=tf.keras.optimizers.Adagrad(),
                      loss=tf.keras.losses.MeanSquaredLogarithmicError(),
                      metrics=tf.keras.metrics.AUC())
        model.set_weights(weights)
    else:
        # Defining nodes quantities
        input_units = dataframe_size
        output_units = 4
        hidden_units = input_units

        # Input layer
        model.add(tf.keras.layers.Dense(units=input_units, activation='relu'))

        # Hidden layers
        model.add(tf.keras.layers.Dense(units=hidden_units))
        model.add(tf.keras.layers.LeakyReLU())
        model.add(tf.keras.layers.Dense(units=hidden_units))
        model.add(tf.keras.layers.LeakyReLU())

        # Output layer
        model.add(tf.keras.layers.Dense(units=output_units, activation='sigmoid'))

        # Create the ANN
        model.compile(optimizer='Adagrad', loss='poisson', metrics=['accuracy'])

    # Feed data to Neural Network
    # NOTE: Lookup 'Mixed Data' Neural Network

    # Train the model
    model.fit(x_train, y_train, batch_size=len(x_train), epochs=1000)

    # Save the model
    save(model, filepath_saved_model + filename_saved_model)

    # Evaluate prediction accuracy of the model
    prediction = model.predict(x_test)

    # Plot the results
    plt.scatter(prediction, y_test)
    plt.xticks([])
    plt.yticks([])
    plt.show()

    for i, p in enumerate(prediction):
        for j, q in enumerate(p):
            if q < 0.00005:
                prediction[i][j] = 0
            else:
                prediction[i][j] = f'{q:.4f}'

    # Save predict and test results to a csv file
    toolbox.dataset_to_csv(filepath_prediction + 'prediction.csv', prediction)
    toolbox.dataset_to_csv(filepath_prediction + 'y_test.csv', y_test)


# Save a machine learning model
def save(model, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    pk.dump(model, open(filepath, 'wb'))


# Load a machine learning model
def load(filepath):
    model = pk.load(open(filepath, 'rb'))
    return model


def plot():
    estimated_fitness = np.array(toolbox.csv_reader(filepath_prediction + 'prediction.csv'))
    actual_fitness = np.array(toolbox.csv_reader(filepath_prediction + 'y_test.csv'))

    print(estimated_fitness[:, 0])

    plt.scatter(estimated_fitness[:, 0], actual_fitness[:, 0])
    plt.xticks([])
    plt.yticks([])
    plt.show()


def evaluate():
    # Import desired outputs
    hdv_fit = HDV_LIG14.hdv_fitness
    hdv_del = HDV_LIG14.hdv_delta
    lig_fit = HDV_LIG14.ligase_fitness
    lig_del = HDV_LIG14.ligase_delta

    # Todo: Recode, inefficient
    hdv_flat = [hdv_fit, hdv_del]
    hdv_flat = np.transpose(hdv_flat)
    hdv_flat = toolbox.dataset_to_csv(filepath_flat + 'hdv_flat.csv', hdv_flat)

    # Read Data
    nt_flat = pd.DataFrame(toolbox.csv_reader(filepath_flat + 'nt_flat.csv'))

    # Convert types
    hdv_flat = np.asarray(hdv_flat).astype('float32')
    # nt_flat = np.asarray(nt_flat).astype(np.int_)

    # Predict the whole set to evaluate the rank of each result.
    # Knn will be applied to determine a rank on unranked data.
    model = load(filepath_saved_model + filename_saved_model)
    pred = model.predict(nt_flat)

    # percent_error = abs((pred[:, 0] - hdv_flat[:, 0])) / hdv_flat[:, 0] * 100
    # toolbox.dataset_to_csv('csv/prediction/percent_error.csv',percent_error)

    plt.scatter(pred[:, 0], hdv_flat[:, 0])
    plt.xticks([])
    plt.yticks([])
    plt.draw()


def test():
    print("Testing HDV-LIG14 Neural Network...")

    # Testing Neural Network
    i = 0
    while i < 200:
        neural_network()
        i += 1

    # evaluate()
    # plot()


# References:
# https://stackoverflow.com/questions/60996892/how-to-replace-loss-function-during-training-tensorflow-keras
