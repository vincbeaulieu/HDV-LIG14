import toolbox
import data_properties as dt
import fasta_gen
import extractor
import encoder as enc
import neural_network

import data_extractor.position_extractor as pe


def main():
    # toolbox.test()
    # dt.test()
    
    # fasta_gen.test()
    # extractor.test()
    # enc.test()
    # neural_network.test()
    
    pe.position_extractor()

    pass

if __name__ == '__main__':
    main()