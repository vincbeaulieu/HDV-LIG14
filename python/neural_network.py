
import matplotlib as plt
import numpy as np
import pandas as pd
import tensorflow as tf

# bpRNA: large-scale automated annotation and analysis of RNA secondary structure
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6009582/

def neural_network():

    seq_amount = 16384

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

        # TODO : Feed data to 'Mixed Data' Neural Network

        gen_index += 1

    pass

def test():
    print("Testing HDV-LIG14 Neural Network...")

    # Testing Neural Network
    neural_network()

    pass

