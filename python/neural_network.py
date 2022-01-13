from scipy.sparse import data
import data as dt
import numpy as np
import pandas as pd
from tensorflow import keras as tfk
import os

import concurrent.futures as ccf

# bpRNA: large-scale automated annotation and analysis of RNA secondary structure
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6009582/

# Create Pandas DataFrame and save output to CSV
def dataset_to_csv(filepath, dataset):
    dataframe = pd.DataFrame(dataset)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    dataframe.to_csv(filepath, index=False, header=False)
    return dataframe

# Read saved files
def reader(filepath):
    lines = []
    with open(filepath, 'r') as file:
        for line in file:
            lines.append(line)
    file.close()
    return lines

# Merge groups of n rows together. 
def merge(lines,n):
    index = 0
    tmp_flat = []
    flat_array = []
    for line in lines:
        if index == 0:
            tmp_flat = line[:-1].split(",")
        elif index % n != 0:
            tmp_flat = [*tmp_flat, *line[:-1].split(",")] 
        else:
            flat_array.append(tmp_flat)
            tmp_flat = line[:-1].split(",")
        index += 1
    flat_array.append(tmp_flat)
    return flat_array

# One Hot Encoder
def one_hot_encoder(sequence,categories,scale=None,remove_last=True):
    scale = (scale,len(categories))[scale==None]
    mapping = dict(zip(categories, range(scale)))
    results = [mapping[i] for i in sequence]
    output = np.rot90(np.eye(scale)[results])
    return (output,output[:-1])[remove_last]

# Dot-Bracket Encoder
def dot_bracket_encoder(sequence,categories=None):

    # Four pairs of brackets
    categories = ["(.)","[.]","{.}","<.>"]

    # open-bracket is +1, close-braket is -1, dots is +0
    values = [1.0, 0.0, -1.0]

    # Bracket Mapping
    round_map = dict(zip(categories[0], values))
    square_map = dict(zip(categories[1], values))
    curly_map = dict(zip(categories[2], values))
    angle_map = dict(zip(categories[3], values))

    # Populate the categories
    R = []; S = []; C = []; A = []
    for i in sequence:
        R.append(round_map.get(i,0))
        S.append(square_map.get(i,0))
        C.append(curly_map.get(i,0))
        A.append(angle_map.get(i,0))

    # Stack the 4 categories
    results = np.stack((R,S,C,A),axis=0)
    return results

def extractor():
    ## Feature Extractions and Encoding

    seq_amount = dt.HDV_LIG14.seq_amount

    nt_dataset = []
    db_dataset = []
    kt_dataset = []
    lp_dataset = []

    # Extract Features
    gen_index = 0
    while gen_index < seq_amount:
        sequence_file = 'st/SEQUENCE_' + str(gen_index) + '.st'
        lines = reader(sequence_file)

        # Check for '#Warning:', while first char is '#', shift down reading index
        shift = 0
        while lines[3 + shift][0] == '#': shift += 1

        # Extract data from '.st' file into strings, except '\n' at the end
        nt_str = lines[3 + shift][:-1]
        db_str = lines[4 + shift][:-1]
        kt_str = lines[5 + shift][:-1]
        lp_str = lines[6 + shift][:-1]

        # Append to dataset arrays
        nt_dataset.append(nt_str)
        db_dataset.append(db_str)
        kt_dataset.append(kt_str)
        lp_dataset.append(lp_str)

        gen_index += 1
    
    # Export dataset to csv
    nt_dataframe = dataset_to_csv('csv/dataset/nt_dataset.csv',nt_dataset)
    db_dataframe = dataset_to_csv('csv/dataset/db_dataset.csv',db_dataset)
    kt_dataframe = dataset_to_csv('csv/dataset/kt_dataset.csv',kt_dataset)
    lp_dataframe = dataset_to_csv('csv/dataset/lp_dataset.csv',lp_dataset)



    # Encoded Arrays
    nt_encoded = []
    db_encoded = []
    kt_encoded = []
    lp_encoded = []
    
    # Catch thread exception, if any
    ExceptionHandler = []
    def encoder_thread(encoded_file,encoded_list,encoder,sequences,categories=None):
        try:
            i = 0
            while i < len(sequences):
                for hot in encoder(sequences[i],categories):
                    encoded_list.append(hot)
                    print("\rSEQUENCE_" + str(i) + " -- Done -- ", end='')
                i += 1
            dataset_to_csv(encoded_file,encoded_list)
            return encoded_list
        except Exception as e:
            ExceptionHandler.append(e)

    # Encode Data (Multi-threaded)
    with ccf.ThreadPoolExecutor() as executor:
            nt_task = executor.submit(encoder_thread, 'csv/encoded/nt_encoded.csv', nt_encoded, one_hot_encoder, dt.HDV_LIG14.genotypes, "ATCG")
            db_task = executor.submit(encoder_thread, 'csv/encoded/db_encoded.csv', db_encoded, dot_bracket_encoder, db_dataset)
            kt_task = executor.submit(encoder_thread, 'csv/encoded/kt_encoded.csv', kt_encoded, one_hot_encoder, kt_dataset, "BEHIMSX")
            lp_task = executor.submit(encoder_thread, 'csv/encoded/lp_encoded.csv', lp_encoded, one_hot_encoder, lp_dataset, "NK")   
    
    # Raise exception, if any
    for e in ExceptionHandler: raise(e)

    # Multi-Threading:
    # https://www.tutorialspoint.com/python/python_multithreading.htm

    # NOTE:
    # * The dataset may have been wrongly generated due to an error in the instruction guide. Regeneration of the dataset will retake place using the previously written SPOT-RNA auto generator program, available in the "git" folder. An additional flag may be added to extract even more features. Extraction will take place on both the HDV-Lib14-RNA and LIG-Lib14-RNA sequences. Therefore, the size of the datasets will at least double.
    # * Nucleotide encoder may further be improved by using the corresponding IUPAC nt. This may be something to explore.
    # * Further extract and scale the data may improve results, such as removing unchanging nodes/variables from the dataset.csv. Perhaps, a scaled/xx_datasets.csv.

def neural_network():
    # Import desired outputs
    hdv_fit = dt.HDV_LIG14.hdv_fitness
    hdv_del = dt.HDV_LIG14.hdv_delta
    lig_fit = dt.HDV_LIG14.ligase_fitness
    lig_del = dt.HDV_LIG14.ligase_delta

    # Flatten the data
    nt_flat = []
    lines = reader('csv/encoded/nt_encoded.csv')
    nt_flat = merge(lines,3)
    nt_flat = dataset_to_csv('csv/flat/nt_flat.csv',nt_flat)

    db_flat = []
    lines = reader('csv/encoded/db_encoded.csv')
    db_flat = merge(lines,4)
    db_flat = dataset_to_csv('csv/flat/db_flat.csv',db_flat)

    kt_flat = []
    lines = reader('csv/encoded/kt_encoded.csv')
    kt_flat = merge(lines,6)
    kt_flat = dataset_to_csv('csv/flat/kt_flat.csv',kt_flat)
    
    lp_flat = []
    lines = reader('csv/encoded/lp_encoded.csv')
    lp_flat = merge(lines,1)
    lp_flat = dataset_to_csv('csv/flat/lp_flat.csv',lp_flat)

    hdv_flat = [hdv_fit, hdv_del]
    hdv_flat = np.transpose(hdv_flat)
    hdv_flat = dataset_to_csv('csv/flat/hdv_flat.csv',hdv_flat)

    # TODO: fixing error:
    # ValueError: Failed to convert a NumPy array to a Tensor (Unsupported object type float).

    # ANN for NT Data
    from sklearn.model_selection import train_test_split
    in_train, in_test, out_train, out_test = train_test_split(nt_flat, hdv_flat, test_size=1/10, random_state=0)
    # NOTE: 10-fold crossvalidation may be implemented 

    ## ann stand for Artificial Neural Network
    nt_ann = tfk.models.Sequential()

    # Nucleotide input layer
    nt_ann.add(tfk.layers.Dense(units=42, activation='relu'))

    # 2 stack of hidden layers
    nt_ann.add(tfk.layers.Dense(units=14, activation='relu'))
    nt_ann.add(tfk.layers.Dense(units=14, activation='relu'))

    # Output layer
    nt_ann.add(tfk.layers.Dense(units=2, activation='sigmoid'))

    # Generate the ANN
    nt_ann.compile( optimizer = 'adam', 
                    loss = 'binary_crossentropy', 
                    metrics = ['accuracy'] )
    
    # Feed data to Neural Network
    # NOTE: Lookup 'Mixed Data' Neural Network
    nt_ann.fit(in_train, out_train, batch_size = 32, epochs = 100)

    prediction = nt_ann.predict(in_test)
    print(np.concatenate((prediction.reshape(len(prediction),1), out_test.reshape(len(out_test),1)),1))
    
    # Making the Confusion Matrix
    from sklearn.metrics import confusion_matrix, accuracy_score
    print(confusion_matrix(out_test, prediction))
    accuracy_score(out_test, prediction)

def test():
    print("Testing HDV-LIG14 Neural Network...")

    # Testing Neural Network
    # extractor()
    neural_network()

    pass
