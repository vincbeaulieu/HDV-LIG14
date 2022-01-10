
from pandas.core.indexes import category
import data as dt
import matplotlib as plt
import numpy as np
import pandas as pd
import tensorflow as tf
import os

# bpRNA: large-scale automated annotation and analysis of RNA secondary structure
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6009582/

def neural_network():

    seq_amount = dt.HDV_LIG14.seq_amount

    nt_dataset = []
    db_dataset = []
    kt_dataset = []
    lp_dataset = []

    # Extract Features
    gen_index = 0
    while gen_index < seq_amount:
        lines = []
        sequence = 'st/SEQUENCE_' + str(gen_index) + '.st'
        with open(sequence, 'r') as st_file:
            for line in st_file:
                lines.append(line)

        # Check for '#Warning:', while first char is '#', shift down reading index
        shift = 0
        while lines[3 + shift][0] == '#': shift += 1

        # Extract data from '.st' file into strings, except '\n' at the end
        nt_str = lines[3 + shift][:-1]
        db_str = lines[4 + shift][:-1]
        kt_str = lines[5 + shift][:-1]
        lp_str = lines[6 + shift][:-1]

        # Convert to arrays
        # nt_node = list(nt_str) # nucleotides sequences
        # db_node = list(db_str) # dot-parens (dot-brackets) notation
        # kt_node = list(kt_str) # knots
        # lp_node = list(lp_str) # loops

        # Append to dataset arrays
        nt_dataset.append(nt_str)
        db_dataset.append(db_str)
        kt_dataset.append(kt_str)
        lp_dataset.append(lp_str)

        gen_index += 1

    # Create Pandas DataFrame and save output to CSV
    def dataset_to_csv(filepath, dataset):
        dataframe = pd.DataFrame(dataset)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        dataframe.to_csv(filepath, index=False, header=False)
        return dataframe
    
    # Export dataset to csv
    nt_dataframe = dataset_to_csv('csv/dataset/nt_dataset.csv',nt_dataset)
    db_dataframe = dataset_to_csv('csv/dataset/db_dataset.csv',db_dataset)
    kt_dataframe = dataset_to_csv('csv/dataset/kt_dataset.csv',kt_dataset)
    lp_dataframe = dataset_to_csv('csv/dataset/lp_dataset.csv',lp_dataset)

    # Import desired outputs
    hdv_fit = dt.HDV_LIG14.hdv_fitness
    hdv_del = dt.HDV_LIG14.hdv_delta
    lig_fit = dt.HDV_LIG14.ligase_fitness
    lig_del = dt.HDV_LIG14.ligase_delta

    ## NOTE:
    # * The neural network for the HDV sequences will be implemented first.
    # * The neural network for the LIG sequences will be implemented in the
    # * future when all the data will be regenerated using the correct indexing.

    # One Hot Encode Data
    def one_hot_encoder(sequence,categories,scale=None,remove_last=True):
        scale = (scale,len(categories))[scale==None]
        mapping = dict(zip(categories, range(scale)))    
        onehotseq = [mapping[i] for i in sequence]
        output = np.rot90(np.eye(scale)[onehotseq])
        return (output,output[:-1])[remove_last]

    # TODO: open-bracket is +1, close-braket is -1, dots is +0, in a hot format
    def incremental_hot_encoder(sequence,categories,scales,remove_last=True):
        # scales, categories: [increment, decrement, constant]
        map_incr = dict(zip(categories[0], range(scales[0])))
        map_decr = dict(zip(categories[1], range(scales[1])))
        map_const = dict(zip(categories[2], range(scales[2])))

        # counters:
        i = 0
        d = 0
        c = 0

        # TODO: To be continued...

        pass

    nt_encoded = []
    db_encoded = []
    kt_encoded = []
    lp_encoded = []
    
    i = 0
    while i < seq_amount:
        # NT Categories: ['A','T/U','C','G']
        for hot in one_hot_encoder(dt.HDV_LIG14.genotypes[i],"ATCG"):
            nt_encoded.append(hot)

        # DB Categories: [['{','(','<','['],[']','>',')','}'],['.']]
        # TODO: 
        #   The encoding of Dot-Bracket will be a sort of incremental-hot encoding.
        #   Where open-bracket is +1, close-braket is -1, dots is +0
        categories = [['{','(','<','['],[']','>',')','}'],['.']]
        incremental_hot_encoder(db_dataset[i],categories,[4,4,1])

        # KT Categories: ['B','E','H','I','M','S','X']
        for hot in one_hot_encoder(kt_dataset[i],"BEHIMSX"):
            kt_encoded.append(hot)

        # LP Categories: ['N','K']
        lp_encoded.append(one_hot_encoder(lp_dataset[i],"NK")[0])

        i += 1

    dataset_to_csv('csv/encoded/nt_encoded.csv',nt_encoded)
    dataset_to_csv('csv/encoded/db_encoded.csv',db_encoded)
    dataset_to_csv('csv/encoded/kt_encoded.csv',kt_encoded)
    dataset_to_csv('csv/encoded/lp_encoded.csv',lp_encoded)

    # Multi-Threading:
    # https://www.tutorialspoint.com/python/python_multithreading.htm

    # Feature Extractions and Encoding
    # * The dataset may have been wrongly generated due to an error in the instruction guide. Regeneration of the dataset will retake place using the previously written SPOT-RNA auto generator program, available in the "git" folder. An additional flag may be added to extract even more features. Extraction will take place on both the HDV-Lib14-RNA and LIG-Lib14-RNA sequences. Therefore, the size of the datasets will at least double.
    # * Dot-bracket encoder is not completed, see "TODO" sections.
    # * Nucleotide encoder may be further improved by using the corresponding IUPAC nt. This may be something to explore.
    # * Implement multi-threading!


    # TODO : Feed data to 'Mixed Data' Neural Network

    pass

def test():
    print("Testing HDV-LIG14 Neural Network...")

    # Testing Neural Network
    neural_network()

    pass

test()

