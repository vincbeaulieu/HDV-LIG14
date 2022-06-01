import data as dt
import toolbox
import encoder as enc

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# import tensorflow as tf
from tensorflow import keras as tfk
# print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

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
    nt_size = len(nt_flat.axes[1])

    db_flat = []
    lines = toolbox.reader('csv/encoded/db_encoded.csv')
    db_flat = toolbox.merge(lines,4)
    db_flat = toolbox.dataset_to_csv('csv/flat/db_flat.csv',db_flat)
    db_size = len(db_flat.axes[1])

    kt_flat = []
    lines = toolbox.reader('csv/encoded/kt_encoded.csv')
    kt_flat = toolbox.merge(lines,6)
    kt_flat = toolbox.dataset_to_csv('csv/flat/kt_flat.csv',kt_flat)
    kt_size = len(kt_flat.axes[1])

    lp_flat = []
    lines = toolbox.reader('csv/encoded/lp_encoded.csv')
    lp_flat = toolbox.merge(lines,1)
    lp_flat = toolbox.dataset_to_csv('csv/flat/lp_flat.csv',lp_flat)
    lp_size = len(lp_flat.axes[1])

    hdv_flat = [hdv_fit, hdv_del, lig_fit, lig_del]
    hdv_flat = np.transpose(hdv_flat)
    hdv_flat = toolbox.dataset_to_csv('csv/flat/hdv_flat.csv',hdv_flat)

    dataframe = nt_flat
    #dataframe = pd.concat([nt_flat,db_flat,kt_flat,lp_flat], axis=1)
    dataframe_size = len(dataframe.axes[1])
    print(dataframe)
    print(dataframe_size)
    dataframe = np.asarray(dataframe).astype(np.byte)
    print(dataframe)
    hdv_flat = np.asarray(hdv_flat).astype('float32')
    
    # ANN for NT Data
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(dataframe, hdv_flat, test_size=1/10, random_state=0)
    # NOTE: 10-fold crossvalidation may be implemented 

    ## Artificial Neural Network
    model = tfk.models.Sequential()
    

    input_units = dataframe_size
    output_units = 4
    hidden_units = (input_units + output_units) * (2/3)

    # Nucleotide input layer
    model.add(tfk.layers.Dense(units=input_units, activation='relu'))

    # Hidden layers
    model.add(tfk.layers.Dense(units=hidden_units, activation='relu'))
    model.add(tfk.layers.Dense(units=hidden_units, activation='relu'))

    # Output layer
    model.add(tfk.layers.Dense(units=output_units, activation='sigmoid'))

    # Generate the ANN
    model.compile(optimizer = 'Adagrad', loss = 'poisson', metrics = ['accuracy'])

    # Feed data to Neural Network
    # NOTE: Lookup 'Mixed Data' Neural Network
    model.fit(x_train, y_train, batch_size = len(x_train), epochs = 1000)

    prediction = model.predict(x_test)

    for i, p in enumerate(prediction):
        for j, q in enumerate(p):
            if q < 0.00005: prediction[i][j] = 0
            else:
                prediction[i][j] = f'{q:.4f}'
    
    toolbox.dataset_to_csv('csv/prediction/prediction.csv',prediction)
    toolbox.dataset_to_csv('csv/prediction/y_test.csv',y_test)

    save(model,'pkl/nt_MachineLearning_model.pkl')
    
    model = load('pkl/nt_MachineLearning_model.pkl')
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

    plt.scatter(estimated_fitness[:,0],actual_fitness[:,0])
    plt.xticks([])
    plt.yticks([])
    plt.show()
    
    pass

def evaluate():
    # Import desired outputs
    hdv_fit = dt.HDV_LIG14.hdv_fitness
    hdv_del = dt.HDV_LIG14.hdv_delta
    lig_fit = dt.HDV_LIG14.ligase_fitness
    lig_del = dt.HDV_LIG14.ligase_delta

    nt_flat = []
    lines = toolbox.reader('csv/encoded/nt_encoded.csv')
    nt_flat = toolbox.merge(lines,3)
    nt_flat = toolbox.dataset_to_csv('csv/flat/nt_flat.csv',nt_flat)

    hdv_flat = [hdv_fit, hdv_del]
    hdv_flat = np.transpose(hdv_flat)
    hdv_flat = toolbox.dataset_to_csv('csv/flat/hdv_flat.csv',hdv_flat)

    nt_flat = np.asarray(nt_flat).astype(np.int_)
    hdv_flat = np.asarray(hdv_flat).astype('float32')

    # Predict the whole set to evaluate the rank of each results.
    # Knn will be applied to determine a rank on unranked data.
    model = load('pkl/nt_MachineLearning_model.pkl')
    pred = model.predict(nt_flat)

    percent_error = abs((pred[:,0] - hdv_flat[:,0]))/hdv_flat[:,0] * 100
    #toolbox.dataset_to_csv('csv/prediction/percent_error.csv',percent_error)

    plt.scatter(pred[:,0],hdv_flat[:,0])
    plt.xticks([])
    plt.yticks([])
    plt.show()
    
    pass

def test():
    print("Testing HDV-LIG14 Neural Network...")

    # Testing Neural Network
    #neural_network()
    evaluate()
    plot()
    pass

test()