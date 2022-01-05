
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

        # TODO : Check for #Warnings on line 3, if first char is not 'G', then add one line

        # Extract specific lines from '.st' file
        nt_seq = lines[3] #nucleotides sequences
        db_not = lines[4] #dot-parens (dot-brackets) notation
        knots = lines[5]
        loops = lines[6]

        # Extract into array
        nt_node = list(nt_seq)
        db_node = list(db_not)
        kt_node = list(knots)
        lp_node = list(loops)

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
    neural_network()
    pass

