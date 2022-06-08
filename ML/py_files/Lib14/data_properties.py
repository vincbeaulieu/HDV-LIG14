
from http.client import NON_AUTHORITATIVE_INFORMATION
import os
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
print(currentdir)
import sys
parentdir = os.path.dirname(currentdir)
rootdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)

## TODO: The Above import is temporary, but used while the .venv and setup.py are implemented.
########

import pandas as pd

# This decorator configuration allow for mutability within objects
# as opposed to @staticmethod. However, @staticmethod should run faster.
def classproperty(func):
   return classmethod(property(func))

class HDV_LIG14():

    #--- Data ---#

    @classproperty
    def col_names(self):
        return ['Sequence',
                'Genotype',
                'HDV_fitness',
                'HDV_delta',
                'Ligase_fitness',
                'Ligase_delta']
    
    @classproperty
    def dataframe(self):
        # The CSV file was extracted with Excel
        return pd.read_csv(rootdir + "/" +'raw/'+'HDV-LIG14_fitness_table.csv',
                                     usecols=self.col_names[:])

    @classproperty
    def dataset(self):
        return self.dataframe.to_numpy()

    @classproperty
    def hdv_rna_sequence(self):
        # HDV_Lib14_RNA
        return  'GGACCATTCGAMTCCCATTAGRCTGGKCCGCCTCCTSGCGGCGG' \
                'GAGTTGSGCKAGGGAGGAASAGYCTTYYCTAGRCTAASGMSCAT' \
                'CGATCCGGTTCGCCGGATCCAAATCGGGCTTCGGTCCGGTTC'
    
    @classproperty
    def lig_rna_sequence(self):
        # LIG_Lib14_RNA
        return  'GGAMTCCCATTAGRCTGGKCCGCCTCCTSGCGGCGGGAGTTGSG' \
                'CKAGGGAGGAASAGYCTTYYCTAGRCTAASGMSCATCGATCCGG' \
                'TTCGCCGGATCCAAATCGGGCTTCGGTCCGGTTC'

    @classproperty
    def hdv_nt_position(self):
        # nt stand for nucleotide
        # Old Data:
        # return [0, 11, 12, 20, 22, 26, 27, 36, 37, 53, 54, 63,
        #        64, 66, 67, 70, 72, 76, 77, 81, 82, 83, 85, 129]
        #
        # Data obtained from position_extractor.py with hdv_nt_pos[:,2]
        return ['11' '21' '26' '36' '50' '53' '63' '66' '70' '71' '76' '81' '83' '84']
    
    @classproperty
    def lig_nt_position(self):
        # nt stand for nucleotide
        # Data obtained from position_extractor.py with lig_nt_pos[:,2]
        return ['3' '13' '18' '28' '42' '45' '55' '58' '62' '63' '68' '73' '75' '76']

    #--- Dataset getters ---#

    @classproperty
    def sequences(self):
        # return the sequence index
        return self.dataset[:, 0]
    
    @classproperty
    def genotypes(self):
        return self.dataset[:, 1]
    
    @classproperty
    def hdv_fitness(self):
        return self.dataset[:, 2]

    @classproperty
    def hdv_delta(self):
        return self.dataset[:, 3]

    @classproperty
    def ligase_fitness(self):
        return self.dataset[:, 4]

    @classproperty
    def ligase_delta(self):
        return self.dataset[:, 5]            

    #--- Attributes ---#

    @classproperty
    def seq_amount(self):
        # return library array length
        return 16384

    pass


def test():
    # Data fetch
    print(HDV_LIG14.col_names)
    print(HDV_LIG14.dataframe)
    print(HDV_LIG14.dataset)
    print(HDV_LIG14.hdv_rna_sequence)
    print(HDV_LIG14.hdv_nt_position)

    # Dataset getters
    print(HDV_LIG14.sequences)
    print(HDV_LIG14.genotypes)
    print(HDV_LIG14.hdv_fitness)
    print(HDV_LIG14.hdv_delta)
    print(HDV_LIG14.ligase_fitness)
    print(HDV_LIG14.ligase_delta)

    # Attribute
    print(HDV_LIG14.seq_amount)

    # extractor() # See Below

    pass


if __name__ == '__main__':
    test()
    print(HDV_LIG14.genotypes)
    pass
