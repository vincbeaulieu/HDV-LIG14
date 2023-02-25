import toolbox
import Lib14.data_properties as dt
import data_extractor.fasta_gen as fasta_gen
import extractor
import encoder as enc
import neural_network

import data_extractor.position_extractor as pe

import tensorflow as tf
import multiprocessing
import psutil 

# Get system stats
nb_cores = psutil.cpu_count()
nb_threads = multiprocessing.cpu_count()

print(tf.__version__)
print(tf.config.list_physical_devices())

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
print("Num CPUs Available: ", len(tf.config.list_physical_devices('CPU')))
print("Num CPU Cores Available: ", nb_cores)
print("Num Threads per CPU Core: ",  int(nb_threads/nb_cores))
print("Num CPU Threads Available: ", nb_threads)


physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)


if __name__ == '__main__':
        
    # toolbox.test()
    # dt.test()

    # fasta_gen.test()
    # extractor.test()
    # enc.test()
    
    # with tf.device('/GPU:0'):
    # neural_network.test()

    # pe.position_extractor()

    pass
