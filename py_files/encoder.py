from data_properties import HDV_LIG14
import toolbox
import numpy as np
import concurrent.futures as ccf

# bpRNA: large-scale automated annotation and analysis of RNA secondary structure
# https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6009582/

# One Hot Encoder
def one_hot_encoder(sequence,categories,scale=None,remove_last=True):
    scale = (scale,len(categories))[scale==None]
    mapping = dict(zip(categories, range(scale)))
    results = [mapping[i] for i in sequence]
    output = np.rot90(np.eye(scale, dtype=int)[results])
    return (output,output[:-1])[remove_last]

# Dot-Bracket Encoder
def dot_bracket_encoder(sequence,categories=None):

    # Four pairs of brackets
    categories = ["(.)","[.]","{.}","<.>"]

    # open-bracket is +1, close-braket is -1, dots is +0
    values = [1, 0, -1]

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

# Catch thread exception, if any
ExceptionHandler = []

# For Multi-Thread Encoding
def encoder_thread(encoded_file,encoded_list,encoder,sequences,categories=None):
    try:
        i = 0
        while i < len(sequences):
            for hot in encoder(sequences[i],categories):
                encoded_list.append(hot)
                print("\rSEQUENCE_" + str(i) + " -- Done -- ", end='')
            i += 1
        toolbox.dataset_to_csv(encoded_file,encoded_list)
        return encoded_list
    except Exception as e:
        ExceptionHandler.append(e)

def encode_rna():
    # Read datasets
    nt_dataset = toolbox.reader('csv/dataset/nt_dataset.csv')
    db_dataset = toolbox.reader('csv/dataset/db_dataset.csv')
    kt_dataset = toolbox.reader('csv/dataset/kt_dataset.csv')
    lp_dataset = toolbox.reader('csv/dataset/lp_dataset.csv')

    # Encoded Arrays
    nt_encoded = []
    db_encoded = []
    kt_encoded = []
    lp_encoded = []

    # Encode Data (Multi-threaded)
    with ccf.ThreadPoolExecutor() as executor:
        nt_task = executor.submit(encoder_thread, 'csv/encoded/nt_encoded.csv', nt_encoded, one_hot_encoder, HDV_LIG14.genotypes, "ATCG")
        db_task = executor.submit(encoder_thread, 'csv/encoded/db_encoded.csv', db_encoded, dot_bracket_encoder, db_dataset)
        kt_task = executor.submit(encoder_thread, 'csv/encoded/kt_encoded.csv', kt_encoded, one_hot_encoder, kt_dataset, "BEHIMSX")
        lp_task = executor.submit(encoder_thread, 'csv/encoded/lp_encoded.csv', lp_encoded, one_hot_encoder, lp_dataset, "NK")   
    
    # Raise exception, if any
    for e in ExceptionHandler: raise(e)

    # Multi-Threading:
    # https://www.tutorialspoint.com/python/python_multithreading.htm

def test():
    print("Testing HDV-LIG14 Encoder...")

    # Testing RNA Encoder
    encode_rna()

    pass
