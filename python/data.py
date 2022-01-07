

import pandas as pd

class HDV_LIG14():

    def __init__(self):
        self.col_names = ['Sequence',
                          'Genotype',
                          'HDV_fitness',
                          'HDV_delta',
                          'Ligase_fitness',
                          'Ligase_delta']

        # The CSV file was extracted with Excel
        self.dataframe = pd.read_csv('python/HDV-LIG14_fitness_table.csv',
                                     usecols=self.col_names()[:])
        self.dataset = self.dataframe.to_numpy()
        
        # nt stand for nucleotide
        self.rna_sequence = "GGACCATTCGAMTCCCATTAGRCTGGKCCGCCTCCTSGCGGCGGGAGTTGSGCKAGGGAGGAASAGYCTTYYCTAGRCTAASGMSCATCGATCCGGTTCGCCGGATCCAAATCGGGCTTCGGTCCGGTTC"
        self.nt_position = [0, 11, 12, 20, 22, 26, 27, 36, 37, 53, 54, 63, 64, 66, 67, 70, 72, 76, 77, 81, 82, 83, 85, 129]

        pass
    
    @classmethod
    def sequences(self):
        return self.dataset[:, 0]

    @classmethod
    def genotypes(self):
        return self.dataset[:, 1]
    
    @classmethod
    def hdv_fitness(self):
        return self.dataset[:, 2]

    @classmethod
    def hdv_delta(self):
        return self.dataset[:, 3]

    @classmethod
    def ligase_fitness(self):
        return self.dataset[:, 4]

    @classmethod
    def ligase_delta(self):
        return self.dataset[:, 5]
    
    pass

