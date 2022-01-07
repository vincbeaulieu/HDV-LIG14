
import data as dt
import matplotlib as plt
import numpy as np
import pandas as pd
import tensorflow as tf

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

        # Extract specific lines from '.st' file into arrays
        nt_node = list(lines[3 + shift]) # nucleotides sequences
        db_node = list(lines[4 + shift]) # dot-parens (dot-brackets) notation
        kt_node = list(lines[5 + shift]) # knots
        lp_node = list(lines[6 + shift]) # loops

        # Remove '\n' at the end
        nt_node.pop()
        db_node.pop()
        kt_node.pop()
        lp_node.pop()

        # print(nt_node)
        # print(db_node)
        # print(kt_node)
        # print(lp_node)

        # Append to dataset arrays
        nt_dataset.append(nt_node)
        db_dataset.append(db_node)
        kt_dataset.append(kt_node)
        lp_dataset.append(lp_node)

        gen_index += 1

    def dataset_to_csv(filepath, dataset):
        dataframe = pd.DataFrame(dataset)
        dataframe.to_csv(filepath, index=False, header=False)
        return dataframe
    
    # Export dataset to csv
    nt_dataframe = dataset_to_csv('csv/nt_dataset.csv',nt_dataset)
    db_dataframe = dataset_to_csv('csv/db_dataset.csv',db_dataset)
    kt_dataframe = dataset_to_csv('csv/kt_dataset.csv',kt_dataset)
    lp_dataframe = dataset_to_csv('csv/lp_dataset.csv',lp_dataset)

    # Import desired outputs
    hdv_fit = dt.HDV_LIG14.hdv_fitness
    hdv_del = dt.HDV_LIG14.hdv_delta
    lig_fit = dt.HDV_LIG14.ligase_fitness
    lig_del = dt.HDV_LIG14.ligase_delta


    # TODO : Feed data to 'Mixed Data' Neural Network

    pass

def test():
    print("Testing HDV-LIG14 Neural Network...")

    # Testing Neural Network
    neural_network()

    pass

