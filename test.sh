


BOLD='\033[1m'
RED='\033[31m'
NC='\033[0m' # No Color

name=$1

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