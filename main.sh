
# Please run:
# conda activate venv

# name=$1

for name in {12..16383}
do
    echo "Generating SEQUENCE_${name}..."

    cd SPOT-RNA

    python3 SPOT-RNA.py  --inputs sample_inputs/SEQUENCE_${name}.fasta  --outputs 'outputs/' --plots True --motifs True --gpu 0 --cpu 32

    cd -

    sh move.sh ${name}

    sh git_upload.sh ${name}

    sleep 1
done
