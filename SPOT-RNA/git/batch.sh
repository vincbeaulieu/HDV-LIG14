
# Move all four ".sh" script in their parent directory "HDV-LIG14" before running the program. Then, ensure the terminal working directory is "HDV-LIG14".

# Please run:
# conda activate venv

BOLD='\033[1m'
RED='\033[31m'
NC='\033[0m' # No Color

dir=$(pwd)

# sh batch.sh [batch_size] [stating_index]
batch_size=$1 && [ -z "$1" ] && batch_size=1
starting_index=$2 && [ -z "$2" ] && starting_index=0

batch_count=$starting_index

ending_index=16383
commit_size=50 # Max commit size: 100 MB

for name in $( eval echo {$starting_index..$ending_index} )
do
    batch=$(($name % $batch_size))
    if (($batch == 0))
    then
        echo "${BOLD}Generating batch #${batch_count}${NC}"
        cd SPOT-RNA

        python3 SPOT-RNA.py  --inputs sample_inputs/BATCH_SEQUENCE_${batch_count}.fasta  --outputs 'outputs/' --plots True --motifs True --gpu 1 --cpu 16
        sleep 2

        cd -
        ((batch_count+=$batch_size))
    fi

    if test ! -f ${dir}/SPOT-RNA/outputs/SEQUENCE_${name}.dbn
    then
        echo "${RED}${BOLD}SEQUENCE_${name} ${NC}${RED}Fail to Generate Completely. Trying to resolve missing data...${NC}"
        cd SPOT-RNA
        
        python3 SPOT-RNA.py  --inputs sample_inputs/SEQUENCE_${name}.fasta  --outputs 'outputs/' --plots True --motifs True --gpu 1 --cpu 16
        sleep 2
        cd -
    fi

    echo "${BOLD}Adding SEQUENCE_${name}...${NC}"
    
    sh move.sh ${name}
    
    sleep 1
    
    sh git_add.sh ${name}
    
    commit_ready=$(($name % $commit_size))
    start=$(($name - $commit_ready))
    
    if (($commit_ready == commit_size-1)) || (($name == $ending_index))
    then
        echo "Commit is Ready..."
        sh git_upload.sh $start $name
    fi
    
done

# Will only push at the end.
git push


