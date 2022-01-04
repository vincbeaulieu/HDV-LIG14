import pandas as pd

HDV_LIG14 = "GGACCATTCGAMTCCCATTAGRCTGGKCCGCCTCCTSGCGGCGGGAGTTGSGCKAGGGAGGAASAGYCTTYYCTAGRCTAASGMSCATCGATCCGGTTCGCCGGATCCAAATCGGGCTTCGGTCCGGTTC"

def fasta_gen(batch_size=None):
    col_names = ['Genotype',
                 'HDV_fitness',
                 'HDV_delta',
                 'Ligase_fitness']

    # The CSV file was extracted with Excel
    dataframe = pd.read_csv('HDV-LIG14_fitness_table.csv', usecols=col_names[:])
    
    dataset = dataframe.to_numpy()
    
    genotypes = dataset[:, 0]

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

        if batch_size == 1:
            # Create individual file
            fasta_file = 'fasta/SEQUENCE_' + str(gen_index) + '.fasta'

            # Create file or overwrite if it exist
            with open(fasta_file, 'w') as f:
                f.writelines(fasta_name + '\n')
                f.writelines(seq_str + '\n')

        elif batch_size > 1:
            # Create batch file
            if gen_index % batch_size == 0:
                batch += 1
                batch_name = 'batch/' + 'size_' + str(batch_size) + '/BATCH_SEQUENCE_' + str(gen_index) + '.fasta'
                # Create empty file or erase its content
                open(batch_name, 'w').close()
            
            # Append to batch file
            with open(batch_name, 'a') as f:
                f.writelines(fasta_name + '\n')
                f.writelines(seq_str + '\n')

        else:
            # Create single file
            if gen_index == 0:
                # Create empty file or erase its content
                open('HDV-LIG14-Sequences.fasta', 'w').close()

            # Append to single file
            with open('HDV-LIG14-Sequences.fasta', 'a') as f:
                f.writelines(fasta_name + '\n')
                f.writelines(seq_str + '\n')

        gen_index += 1
    
    pass

def test():
    # Testing single file
    fasta_gen()

    # Testing individual files
    fasta_gen(1)

    # Testing batch files
    fasta_gen(100)
    
    pass