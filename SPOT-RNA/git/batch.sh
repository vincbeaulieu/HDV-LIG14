
# Move all four ".sh" script in their parent directory "HDV-LIG14" before running the program. Then, ensure the terminal working directory is "HDV-LIG14".

# Please run:
# conda activate venv

dir=$(pwd)

source ${dir}/SPOT-RNA/git/color.sh
source ${dir}/SPOT-RNA/git/validate_results.sh
source ${dir}/SPOT-RNA/git/relocate.sh
source ${dir}/SPOT-RNA/git/git_add.sh

# COMMAND INFO:
# sh batch_test.sh [batch_size] [stating_index] [dataset_directory]

# Assign default values when arguments are not provided
batch_size=$1 && [ -z "$1" ] && batch_size=1
starting_index=$2 && [ -z "$2" ] && starting_index=0
dataset_directory=$3 && [ -z "$3" ] && dataset_directory="Datasets/tmp"

batch_count=$starting_index
ending_index=16383 # 16383
commit_size=50 # Max commit size: 100 MB

for name in $( eval echo {$starting_index..$ending_index} )
do
    # Will generate a complete batch using SPOT-RNA (Improve performance over generating individual fasta sequence)
    batch=$(($name % $batch_size))
    if (($batch == 0))
    then
        echo "${BOLD}Generating batch #${batch_count}${NC}"
        
        cd SPOT-RNA >/dev/null
        # python3 SPOT-RNA.py  --inputs sample_inputs/BATCH_SEQUENCE_${batch_count}.fasta  --outputs 'outputs/' --plots True --motifs True --gpu 1 --cpu 16
        sleep 2
        cd - >/dev/null
        
        ((batch_count+=$batch_size))
    fi
    
    # Check for missing files and print them in white upon first try
    all_files_present "${dir}/SPOT-RNA/outputs" ${name}; retval=$?
    [ "$retval" -eq 1 ] && echo "${BOLD}${RED}SEQUENCE_${name} Failed to Completely Generate${NC}" # oneline if ... then ...
    IFS=""; printf "%s\n" ${retlog[@]} # IFS set the delimiter for printf

    # Will regenerate missing data using the individual sequence and retry until SPOT-RNA successfully create the files
    until [ $retval -eq 0 ]
    do
        echo "${BOLD}${YELLOW}Trying To Resolve Missing Data${NC}"
        
        cd SPOT-RNA >/dev/null
        # python3 SPOT-RNA.py  --inputs sample_inputs/SEQUENCE_${name}.fasta  --outputs 'outputs/' --plots True --motifs True --gpu 1 --cpu 16
        sleep 2
        cd - >/dev/null
        
        # Check for missing files and print them in red upon retry
        all_files_present "${dir}/SPOT-RNA/outputs" ${name}; retval=$?
        printf "${RED}%s\n${NC}" ${retlog[@]}
    done
    
    # Relocate Data to $dataset_directory
    echo "${GREEN}${MVUP}Relocating SEQUENCE_${name} to $dataset_directory${NC}"
    relocate_copy "${dir}/SPOT-RNA/outputs/SEQUENCE_${name}" "$dataset_directory"
    sleep 1
    
    echo "${GREEN}${MVUP}${DEL}Adding SEQUENCE_${name}${NC}"
    git_add "${dataset_directory}" "SEQUENCE_${name}"
    echo "${GREEN}${BOLD}${MVUP}${DEL}SEQUENCE_${name} Added!${NC}"
    
    commit_ready=$(($name % $commit_size))
    start=$(($name - $commit_ready))
    
    if (($commit_ready == commit_size-1)) || (($name == $ending_index))
    then
        echo "Commit is Ready..."
        # sh git_upload.sh $start $name
    fi
done

# Will only push at the end.
# lookup: git squash --> ref: https://stackoverflow.com/questions/5189560/how-to-squash-my-last-x-commits-together
# git push


