

import numpy as np
import pandas as pd
import tensorflow as tf

def neural_network():

    seq_length = 130
    seq_amount = 16384

    # Extract Data
    gen_index = 0
    while gen_index < seq_amount:
        lines = []
        sequence = 'st/SEQUENCE_' + str(gen_index) + '.st'
        with open(sequence, 'r') as st_file:
            for line in st_file:
                lines.append(line)

        nt_seq = lines[3] #nucleotides sequences
        db_not = lines[4] #dot-parens (dot-brackets) notation
        knots = lines[5]
        loops = lines[6]

        nt_node = list(nt_seq)
        db_node = list(db_not)
        kt_node = list(knots)
        lp_node = list(loops)

        nt_node.pop()
        db_node.pop()
        kt_node.pop()
        lp_node.pop()

        # print(nt_node)
        # print(db_node)
        # print(kt_node)
        # print(lp_node)

        # TODO : Feed data to Neural Network

        gen_index += 1

    pass

def test():
    print("Testing HDV-LIG14 Neural Network...")
    neural_network()
    pass

