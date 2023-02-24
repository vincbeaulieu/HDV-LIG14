
import numpy as np
import pandas as pd
import toolbox
import psutil

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from Lib14.data_properties import HDV_LIG14

import multiprocessing
import multiprocessing.shared_memory
import concurrent.futures

# Define file location of ".prob" files
filepath_prob = "Datasets/HDV/prob/"

# Get and print system stats
nb_cores = psutil.cpu_count()
nb_threads = multiprocessing.cpu_count()
print("Num CPU Cores Available: ", nb_cores)
print("Num CPU Threads Available: ", nb_threads)

# Get the expected output data
hdv_fit = np.array(HDV_LIG14.hdv_fitness)

# Get length of the dataset
len_sequences = HDV_LIG14.seq_amount

# Define the size and shape of your shared memory array
dataset_shape = (len_sequences, 129, 64)
dataset_dtype = np.float32
dataset_size = np.prod(dataset_shape) * np.dtype(dataset_dtype).itemsize

print(np.dtype(dataset_dtype).itemsize)
print(np.prod(dataset_shape))

# Create the shared memory array and wrap it in a numpy array
shm = multiprocessing.shared_memory.SharedMemory(create=True, size=dataset_size)
dataset = np.ndarray(dataset_shape, dtype=dataset_dtype, buffer=shm.buf)




# Output the data onto a ".csv" file
def check_results(data):
    print(data)
    toolbox.dataset_to_csv('ML/py_files/test/matrix.csv', data)
    exit()


def reformat(index):
    # Go through all the ".prob" files
    filename = filepath_prob + "SEQUENCE_" + str(index) + ".prob"

    # Extract data from ".prob" file
    image = np.loadtxt(filename, delimiter="\t")

    # Get matrix indexes of upper triangular part with offset of 2
    indexes = np.triu_indices(130, 2)

    # Reshape the image into a compact format (129 x 64)
    image = np.reshape(image[indexes], (129, 64))

    # Return the data
    return image


# Define workers' job
def worker(works):
    for index in works:
        dataset[index] = reformat(index)


# Extract and reformat the ".prob" data
def process_file(workload):
    # Set number of threads per process
    nb_workers = nb_threads/nb_cores

    # Divide the workload across workers
    workload_per_thread = np.array_split(workload, nb_workers)   

    # Use concurrent.futures to process the data in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=nb_threads) as executor:
        futures = []
        for works in workload_per_thread:
            futures.append(executor.submit(worker, works))
        concurrent.futures.wait(futures)
            
        # Populate the dataset with the processed data
        #for index, future in enumerate(futures):
            #dataset[index] = future.result()

    # Return the dataset
    return dataset


if __name__ == '__main__':
    



    # Initialise dataset
    mydata = np.empty((len_sequences, 129, 64), dtype=np.float32)
    print(mydata.itemsize)

    # Divide the workload
    workload_per_core = np.array_split(range(len_sequences), nb_cores)
    
    # Use multiprocessing to populate the dataset in parallel
    with multiprocessing.Pool(processes=nb_cores) as pool:
        dataset = np.array(pool.map(process_file, workload_per_core))

    # Use the resulting dataset
    print(dataset.shape)

    # shape = data.shape
    # data = np.reshape(data, (shape[0], shape[1], shape[2], 1))

