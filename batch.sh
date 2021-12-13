
# Please run:
# conda activate venv

# name=$1

batch_count=0

for name in {1320..16383}
do
    batch=$(($name%20))
    if (($batch == 0))
    then
        echo "Generating batch #${batch_count}"
        cd SPOT-RNA

        python3 SPOT-RNA.py  --inputs sample_inputs/batch_sequence_${batch_count}.fasta  --outputs 'outputs/' --plots True --motifs True --gpu 0 --cpu 32

        cd -
        ((batch_count++))
    fi
    
    echo "Uploading SEQUENCE_${name}..."
    
    sh move.sh ${name}

    sh git_upload.sh ${name}

    sleep 1
    
done
