import toolbox
import Lib14.data_properties as dt
import data_extractor.fasta_gen as fasta_gen
import extractor
import encoder as enc
import neural_network

import data_extractor.position_extractor as pe

import tensorflow as tf

print(tf.__version__)
print(tf.config.list_physical_devices())

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], True)

def main():



        
    # toolbox.test()
    # dt.test()

    # fasta_gen.test()
    # extractor.test()
    # enc.test()
    
    # with tf.device('/GPU:0'):
    neural_network.test()

    # pe.position_extractor()


if __name__ == '__main__':
    main()
