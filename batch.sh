
# Please run:
# conda activate venv

BOLD='\033[1m'
RED='\033[31m'
NC='\033[0m' # No Color

# name=$1
dir=$(pwd)

batch_count=1480

for name in {1480..16383}
do
    batch=$(($name%20))
    if (($batch == 0))
    then
        echo "${BOLD}Generating batch #${batch_count}${NC}"
        cd SPOT-RNA

        python3 SPOT-RNA.py  --inputs sample_inputs/batch_sequence_${batch_count}.fasta  --outputs 'outputs/' --plots True --motifs True --gpu 0 --cpu 32
        sleep 2

        cd -
        ((batch_count+=20))
    fi

    if test ! -f ${dir}/SPOT-RNA/outputs/SEQUENCE_${name}.dbn
    then
        echo "${RED}${BOLD}SEQUENCE_${name} ${NC}${RED}Fail to Generate Completely. Trying to resolve missing data...${NC}"
        cd SPOT-RNA
        python3 SPOT-RNA.py  --inputs sample_inputs/SEQUENCE_${name}.fasta  --outputs 'outputs/' --plots True --motifs True --gpu 0
        sleep 2
        cd -
    fi

    echo "${BOLD}Uploading SEQUENCE_${name}...${NC}"
    
    sh move.sh ${name}

    sleep 1

    sh git_upload.sh ${name}
    
done
