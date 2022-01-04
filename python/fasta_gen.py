import pandas as pd
import os

HDV_LIG14 = "GGACCATTCGAMTCCCATTAGRCTGGKCCGCCTCCTSGCGGCGGGAGTTGSGCKAGGGAGGAASAGYCTTYYCTAGRCTAASGMSCATCGATCCGGTTCGCCGGATCCAAATCGGGCTTCGGTCCGGTTC"

def fasta_gen(batch_size=None):
    col_names = ['Sequence',
                 'Genotype',
                 'HDV_fitness',
                 'HDV_delta',
                 'Ligase_fitness',
                 'Ligase_delta']

    # The CSV file was extracted with Excel
    dataframe = pd.read_csv('python/HDV-LIG14_fitness_table.csv', usecols=col_names[:])
    
    dataset = dataframe.to_numpy()
    
    genotypes = dataset[:, 1]

    # nt stand for nucleotide
    nt_index = [0, 11, 12, 20, 22, 26, 27, 36, 37, 53, 54, 63, 64, 66, 67, 70, 72, 76, 77, 81, 82, 83, 85, 129]

    batch = 0
    gen_index = 0
    while gen_index < len(genotypes):
        sequence = list(HDV_LIG14)

        char_index = 0
        # print(genotypes[gen_index][char_index])

        i = 1
        while i < len(nt_index) - 1:
            _from = nt_index[i]
            _to = nt_index[i + 1]
            _incr = _to - _from

            # print(i, end=' ')
            sequence[_from:_to] = genotypes[gen_index][char_index:char_index + _incr]
            # print(sequence[_from:_to])

            char_index += _incr
            i += 2

        # print(sequence)
        seq_str = ""
        for s in sequence:
            seq_str += s
        # print(seq_str)

        fasta_name = '>SEQUENCE_' + str(gen_index)
        # print(fasta_name)

        if batch_size == None:
            # Create single file
            if gen_index == 0:
                # Create empty file or erase its content
                os.makedirs(os.path.dirname('fasta/HDV-LIG14-Sequences.fasta'), exist_ok=True)
                open('fasta/HDV-LIG14-Sequences.fasta', 'w').close()

            # Append to single file
            with open('fasta/HDV-LIG14-Sequences.fasta', 'a') as f:
                f.writelines(fasta_name + '\n')
                f.writelines(seq_str + '\n')

        elif batch_size == 1:
            # Create individual file
            fasta_file = 'fasta/single/SEQUENCE_' + str(gen_index) + '.fasta'
            os.makedirs(os.path.dirname(fasta_file), exist_ok=True)

            # Create file or overwrite if it exist
            with open(fasta_file, 'w') as f:
                f.writelines(fasta_name + '\n')
                f.writelines(seq_str + '\n')

        elif batch_size > 1:
            # Create batch file
            if gen_index % batch_size == 0:
                batch += 1
                batch_file = 'fasta/batch/' + 'size_' + str(batch_size) + '/BATCH_SEQUENCE_' + str(gen_index) + '.fasta'
                os.makedirs(os.path.dirname(batch_file), exist_ok=True)
                # Create empty file or erase its content
                open(batch_file, 'w').close()
            
            # Append to batch file
            with open(batch_file, 'a') as f:
                f.writelines(fasta_name + '\n')
                f.writelines(seq_str + '\n')

        else:
            print("fasta_gen: Invalid Argument")
            exit(1)
            
        gen_index += 1
    
    pass

def test():
    print("Testing Fasta Generator...")
    
    # Testing single file
    fasta_gen()

    # Testing individual files
    fasta_gen(1)

    # Testing batch files
    fasta_gen(100)
    
    pass