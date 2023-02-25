import concurrent.futures
import multiprocessing
import numpy as np
import psutil

from ML.py_files.Lib14.data_properties import HDV_LIG14
# from brain import cnn

# Define file location of ".prob" files
data_path = "Datasets/HDV/prob/"
save_path = "ML/py_files/cnn_prob/"

# Get system stats
nb_cores = psutil.cpu_count()
nb_threads = multiprocessing.cpu_count()


def extract_image(index):
    # Go through all the ".prob" files
    filename = data_path + "SEQUENCE_" + str(index) + ".prob"

    # Extract data from ".prob" file
    image = np.loadtxt(filename, delimiter="\t")

    # Get matrix indexes of upper triangular part with offset of 2
    indexes = np.triu_indices(130, 2)

    # Reshape the image into a compact format (129 x 64)
    image = np.reshape(image[indexes], (129, 64))

    # Return the data
    return image


# Test function of extract image
def test_data(index):
    return np.full((129, 64), 100000+index)


# Define workers' task
def worker(works):
    jobs = [None] * len(works)
    for i, index in enumerate(works):
        jobs[i] = extract_image(index)
    return list(zip(works, jobs))


# Extract and reformat the ".prob" data
def process(workload):
    # Set the number of threads per process
    nb_workers = nb_threads/nb_cores

    # Divide the workload across workers
    workload_per_thread = np.array_split(workload, nb_workers)   

    # Split further the process into threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=nb_workers) as executor:
        results = list(executor.map(worker, workload_per_thread))

    # Return the dataset
    return results


if __name__ == '__main__':
    # Print system stats
    print("Num CPU Cores Available: ", nb_cores)
    print("Num CPU Threads Available: ", nb_threads)

    # Get the expected output data
    hdv_fit = np.array(HDV_LIG14.hdv_fitness, dtype="float64")

    # Get length of the dataset
    len_sequences = HDV_LIG14.seq_amount

    # Initialise dataset
    dataset = np.empty((len_sequences, 129, 64), dtype=np.float64)

    # Divide the workload
    workload_per_core = np.array_split(range(len_sequences), nb_cores)
    
    # Use multiprocessing to populate the dataset in parallel
    with multiprocessing.Pool(processes=nb_cores) as pool:
        results = np.array(pool.map(process, workload_per_core), dtype=object)
    
    # Combine the results from each core
    results = np.reshape(results, (len_sequences, 2))

    # Populates the dataset in ascending order of sequences 
    for i in range(len_sequences):
        dataset[results[i][0]] = results[i][1]
    
    # Save processed data to numpy file 
    np.save(save_path + 'images.npy', dataset)
    np.save(save_path + 'fitness.npy', hdv_fit)

    # Feed data to CNN
    # cnn(dataset, hdv_fit)