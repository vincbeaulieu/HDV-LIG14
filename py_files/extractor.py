from data_properties import HDV_LIG14
import toolbox

# Data Extraction
def extractor():
    seq_amount = HDV_LIG14.seq_amount

    nt_dataset = []
    db_dataset = []
    kt_dataset = []
    lp_dataset = []

    # Extract features from raw data
    gen_index = 0
    while gen_index < seq_amount:
        sequence_file = 'st/SEQUENCE_' + str(gen_index) + '.st'
        lines = toolbox.reader(sequence_file)

        # Check for '#Warning:', while first char is '#', shift down reading index
        shift = 0
        while lines[3 + shift][0] == '#': shift += 1

        # Extract data from '.st' file into strings, except '\n' at the end
        nt_str = lines[3 + shift]
        db_str = lines[4 + shift]
        kt_str = lines[5 + shift]
        lp_str = lines[6 + shift]

        # Append to dataset arrays
        nt_dataset.append(nt_str)
        db_dataset.append(db_str)
        kt_dataset.append(kt_str)
        lp_dataset.append(lp_str)

        gen_index += 1
    
    # Export dataset to csv
    nt_dataframe = toolbox.dataset_to_csv('csv/dataset/nt_dataset.csv',nt_dataset)
    db_dataframe = toolbox.dataset_to_csv('csv/dataset/db_dataset.csv',db_dataset)
    kt_dataframe = toolbox.dataset_to_csv('csv/dataset/kt_dataset.csv',kt_dataset)
    lp_dataframe = toolbox.dataset_to_csv('csv/dataset/lp_dataset.csv',lp_dataset)

    # NOTE:
    # * The dataset may have been wrongly generated due to an error in the instruction guide. Regeneration of the dataset will retake place using the previously written SPOT-RNA auto generator program, available in the "git" folder. An additional flag may be added to extract even more features. Extraction will take place on both the HDV-Lib14-RNA and LIG-Lib14-RNA sequences. Therefore, the size of the datasets will at least double.
    # * Nucleotide encoder may further be improved by using the corresponding IUPAC nt. This may be something to explore.
    # * Further extract and scale the data may improve results, such as removing unchanging nodes/variables from the dataset.csv. Perhaps, a scaled/xx_datasets.csv.

def test():
    print("Testing HDV-LIG14 Extractor...")

    # Testing Extractor
    extractor()

    pass