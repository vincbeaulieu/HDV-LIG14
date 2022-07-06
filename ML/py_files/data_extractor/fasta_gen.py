import os

from ML.py_files.Lib14.data_properties import HDV_LIG14

# output_dir, if define, include a '/' at the end of the string argument.
def fasta_gen(generic_sequence, rna_nt_pos, output_dir="", filename="sequences", batch_size=None):
    seq_amount = HDV_LIG14.seq_amount
    isolated_rna = HDV_LIG14.genotypes
    g_seq_lst = list(generic_sequence) # generic_sequence_list

    batch = 0
    gen_index = 0
    while gen_index < seq_amount: # 16384

        fasta_name = '>SEQUENCE_' + str(gen_index)
        # print(fasta_name)

        # Replace the character in the generic sequence, which utilize non-singleton nucleotide,
        # with character from the isolated nucleotide sequence, which comprises of only singleton nucleotide (A,T,C,G).
        # The index of the characters to be replaced are given by 'rna_nt_pos', extracted from the position_extractor.py.
        for index, pos_value in enumerate(rna_nt_pos):
            g_seq_lst[pos_value] = isolated_rna[gen_index][index]
        seq_str = "".join(g_seq_lst)
        # print(seq_str)

        if batch_size == None:
            # Define the output directory
            fasta_dir = output_dir + 'fasta/' + filename + '.fasta'

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


def fasta_run(g_seq,nt_pos,out_dir,title):
    print('\033[95m' + "\nRunning " + title + " Fasta Generator")

    # Fasta Generator for HDV Sequences
    print("Creating Fasta Files...")

    # Creating single fasta file
    fasta_gen(g_seq,nt_pos,out_dir,filename=title)

    # Creating individual fasta files
    fasta_gen(g_seq,nt_pos,out_dir,batch_size=1)

    # Creating batch fasta files (batch of 100)
    fasta_gen(g_seq,nt_pos,out_dir,batch_size=100)

    print('\033[92m' + 'Done' + '\033[0m')
    pass


if __name__ == '__main__':

    # HDV fasta generator:
    g_seq = HDV_LIG14.hdv_rna_sequence # generic_sequence
    nt_pos = HDV_LIG14.hdv_nt_position
    out_dir="Datasets/HDV/"
    title = 'HDV-Lib14'

    # Launch Generator for HDV fasta files
    fasta_run(g_seq,nt_pos,out_dir,title)


    # LIG fasta generator:
    g_seq = HDV_LIG14.lig_rna_sequence # generic_sequence
    nt_pos = HDV_LIG14.lig_nt_position
    out_dir="Datasets/LIG/"
    title = 'LIG-Lib14'

    # Launch Generator for LIG fasta files
    fasta_run(g_seq,nt_pos,out_dir,title)

    print()

