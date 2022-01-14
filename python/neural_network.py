import data as dt
import toolbox
import encoder as enc

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

import tensorflow as tf
from tensorflow import keras as tfk
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

def neural_network():
    # Import desired outputs
    hdv_fit = dt.HDV_LIG14.hdv_fitness
    hdv_del = dt.HDV_LIG14.hdv_delta
    lig_fit = dt.HDV_LIG14.ligase_fitness
    lig_del = dt.HDV_LIG14.ligase_delta

    # Dimensionality Reduction
    nt_flat = []
    lines = toolbox.reader('csv/encoded/nt_encoded.csv')
    nt_flat = toolbox.merge(lines,3)
    nt_flat = toolbox.dataset_to_csv('csv/flat/nt_flat.csv',nt_flat)

    db_flat = []
    lines = toolbox.reader('csv/encoded/db_encoded.csv')
    db_flat = toolbox.merge(lines,4)
    db_flat = toolbox.dataset_to_csv('csv/flat/db_flat.csv',db_flat)

    kt_flat = []
    lines = toolbox.reader('csv/encoded/kt_encoded.csv')
    kt_flat = toolbox.merge(lines,6)
    kt_flat = toolbox.dataset_to_csv('csv/flat/kt_flat.csv',kt_flat)
    
    lp_flat = []
    lines = toolbox.reader('csv/encoded/lp_encoded.csv')
    lp_flat = toolbox.merge(lines,1)
    lp_flat = toolbox.dataset_to_csv('csv/flat/lp_flat.csv',lp_flat)

    hdv_flat = [hdv_fit, hdv_del]
    hdv_flat = np.transpose(hdv_flat)
    hdv_flat = toolbox.dataset_to_csv('csv/flat/hdv_flat.csv',hdv_flat)

    # TODO: fixing error:
    # ValueError: Failed to convert a NumPy array to a Tensor (Unsupported object type float).

    nt_flat = np.asarray(nt_flat).astype(np.int_)
    hdv_flat = np.asarray(hdv_flat).astype('float32')
    
    # ANN for NT Data
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(nt_flat, hdv_flat, test_size=1/10, random_state=0)
    # NOTE: 10-fold crossvalidation may be implemented 

    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    #x_train = scaler.fit_transform(x_train)
    #x_test = scaler.transform(x_test)
    #y_train = scaler.fit_transform(x_train)
    #y_test = scaler.transform(x_test)


    ## ann stand for Artificial Neural Network
    model = tfk.models.Sequential()

    # Nucleotide input layer
    model.add(tfk.layers.Dense(units=42, activation='relu'))

    # Hidden layers
    model.add(tfk.layers.Dense(units=168, activation='relu'))
    model.add(tfk.layers.Dense(units=84, activation='relu'))
    model.add(tfk.layers.Dense(units=42, activation='relu'))
    model.add(tfk.layers.Dense(units=14, activation='relu'))

    # Output layer
    model.add(tfk.layers.Dense(units=2, activation='sigmoid'))

    # Generate the ANN
    model.compile(optimizer = 'adam', loss = 'poisson', metrics = ['accuracy'])

    # Feed data to Neural Network
    # NOTE: Lookup 'Mixed Data' Neural Network
    model.fit(x_train, y_train, batch_size = 1024, epochs = 2000)

    prediction = model.predict(x_test)

    for i, p in enumerate(prediction):
        for j, q in enumerate(p):
            if q < 0.00005: prediction[i][j] = 0
            else:
                prediction[i][j] = f'{q:.4f}'
    
    toolbox.dataset_to_csv('csv/prediction/prediction.csv',prediction)
    toolbox.dataset_to_csv('csv/prediction/y_test.csv',y_test)

    save(model,'pkl/nt_MachineLearning.pkl')
    
    model = load('pkl/nt_MachineLearning.pkl')
    print(model.predict(x_test))



import pickle as pk

# Save a machine learning model
def save(model,filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    pk.dump(model, open(filepath,'wb'))

# Load a machine learning model
def load(filepath):
    model = pk.load(open(filepath,'rb'))
    return model


def plot():
    estimated_fitness = np.array(toolbox.csv_reader('csv/prediction/prediction.csv'))
    actual_fitness = np.array(toolbox.csv_reader('csv/prediction/y_test.csv'))
    
    print(estimated_fitness[:,0])
    

    # NOTE: reader does not utilise delimiter - TODO
    plt.scatter(actual_fitness[:,0],estimated_fitness[:,0])
    plt.show()
    pass

def test():
    print("Testing HDV-LIG14 Neural Network...")

    # Testing Neural Network
    neural_network()
    plot()
    pass