
import matplotlib as plt
import numpy as np
import pandas as pd
import tensorflow as tf

# bpRNA: large-scale automated annotation and analysis of RNA secondary structure
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6009582/

def neural_network():

    seq_amount = 16384

    nt_dataset = []
    db_dataset = []
    kt_dataset = []
    lp_dataset = []

    # Extract Data
    gen_index = 0
    while gen_index < seq_amount:
        lines = []
        sequence = 'st/SEQUENCE_' + str(gen_index) + '.st'
        with open(sequence, 'r') as st_file:
            for line in st_file:
                lines.append(line)

        # Check for '#Warning:' on line 3, if first char is '#', then shift down the reading index
        shift = (0,1)[lines[3][0] == '#']

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
        pd.DataFrame(dataset).to_csv(filepath, index=False, header=False)
    
    # Exporting dataset to csv
    dataset_to_csv('csv/nt_dataset.csv',nt_dataset)
    dataset_to_csv('csv/db_dataset.csv',db_dataset)
    dataset_to_csv('csv/kt_dataset.csv',kt_dataset)
    dataset_to_csv('csv/lp_dataset.csv',lp_dataset)

    # TODO : Feed data to 'Mixed Data' Neural Network

    pass

def test():
    print("Testing HDV-LIG14 Neural Network...")

    # Testing Neural Network
    neural_network()

    pass

