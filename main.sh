
# Please run:
# conda activate venv

# name=$1

for name in {12..16383}
do
    echo "Generating SEQUENCE_${name}..."

    cd SPOT-RNA

    x=0
    while [python3 SPOT-RNA.py  --inputs sample_inputs/SEQUENCE_${name}.fasta  --outputs 'outputs/' --plots True --motifs True --gpu 0 --cpu 32 | grep -q 'Unable to run bpRNA script;']
    do
        echo "Sequence generation failed $x"        
        $(( x++ ))
    done
    cd -

    sh move.sh ${name}

    sh git_upload.sh ${name}
done
