import data as dt
import matplotlib as plt
import numpy as np
import pandas as pd
import tensorflow as tf
import os

import concurrent.futures as ccf

# bpRNA: large-scale automated annotation and analysis of RNA secondary structure
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6009582/

def neural_network():
    ## Feature Extractions and Encoding

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

    # Encoded Arrays
    nt_encoded = []
    db_encoded = []
    kt_encoded = []
    lp_encoded = []

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
    
    # Raise Exception if any
    for e in ExceptionHandler: raise(e) 

    # Multi-Threading:
    # https://www.tutorialspoint.com/python/python_multithreading.htm

    # NOTE:
    # * The dataset may have been wrongly generated due to an error in the instruction guide. Regeneration of the dataset will retake place using the previously written SPOT-RNA auto generator program, available in the "git" folder. An additional flag may be added to extract even more features. Extraction will take place on both the HDV-Lib14-RNA and LIG-Lib14-RNA sequences. Therefore, the size of the datasets will at least double.
    # * Nucleotide encoder may further be improved by using the corresponding IUPAC nt. This may be something to explore.

    # TODO : Feed data to 'Mixed Data' Neural Network

    pass

def test():
    print("Testing HDV-LIG14 Neural Network...")

    # Testing Neural Network
    neural_network()

    pass

test()

