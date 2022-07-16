import os

from ML.py_files.Lib14.data_properties import HDV_LIG14

# output_dir, if define, include a '/' at the end of the string argument.
def fasta_gen(rna_seq, rna_nt_pos, output_dir="", batch_size=None):
    print("Hello")

    seq_amount = HDV_LIG14.seq_amount
    genotypes = HDV_LIG14.genotypes

    batch = 0
    gen_index = 0
    while gen_index < seq_amount: # 16384
        sequence = list(rna_seq)

        char_index = 0
        # print(genotypes[gen_index][char_index])

        i = 1
        while i < len(rna_nt_pos) - 1:
            _from = rna_nt_pos[i]
            _to = rna_nt_pos[i + 1]
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
        print(seq_str)

        fasta_name = '>SEQUENCE_' + str(gen_index)
        # print(fasta_name)

        if batch_size == None:
            # Define the Output Directory
            fasta_dir = output_dir + 'fasta/sequences.fasta'

            # Create single file
            if gen_index == 0:
                # Create empty file or erase its content
                os.makedirs(os.path.dirname(fasta_dir), exist_ok=True)
                open(fasta_dir, 'w').close()

            # Append to single file
            with open(fasta_dir, 'a') as f:
                f.writelines(fasta_name + '\n')
                f.writelines(seq_str + '\n')

        elif batch_size == 1:
            # Create individual file
            fasta_file = output_dir + 'fasta/single/SEQUENCE_' + str(gen_index) + '.fasta'
            os.makedirs(os.path.dirname(fasta_file), exist_ok=True)

            # Create file or overwrite if it exist
            with open(fasta_file, 'w') as f:
                f.writelines(fasta_name + '\n')
                f.writelines(seq_str + '\n')

        elif batch_size > 1:
            # Create batch file
            if gen_index % batch_size == 0:
                batch += 1
                batch_file = output_dir + 'fasta/batch/' + 'size_' + str(batch_size) + '/BATCH_SEQUENCE_' + str(gen_index) + '.fasta'
                # Create empty file or erase its content
                os.makedirs(os.path.dirname(batch_file), exist_ok=True)
                open(batch_file, 'w').close()
            
            # Append to batch file
            with open(batch_file, 'a') as f:
                f.writelines(fasta_name + '\n')
                f.writelines(seq_str + '\n')

        else:
            raise ValueError("fasta_gen: Invalid Argument")
            
        gen_index += 1
    
    pass

def launch():
    print("Running HDV-LIG14 Fasta Generator...")

    # Fasta Generator for HDV Sequences
    print("Creating HDV-Lib14 Fasta Files...")

    # Defining arguments
    rna_seq = HDV_LIG14.hdv_rna_sequence
    rna_nt_pos = HDV_LIG14.hdv_nt_position
    output_dir="Datasets/HDV/"

    # Creating HDV single fasta file
    fasta_gen(rna_seq,rna_nt_pos,output_dir)

    # Creating HDV individual fasta files
    # fasta_gen(rna_seq,rna_nt_pos,output_dir,1)

    # Creating HDV batch fasta files (batch of 100)
    # fasta_gen(rna_seq,rna_nt_pos,output_dir,100)

    print("Done\n")
    
    pass

if __name__ == '__main__':
    launch()