
# COMMAND INFO:
# sh batch.sh [batch_size] [stating_index] [dataset_directory] [ending_index] [commit_size]

# Prior to executing the command:
# - Ensure that the terminal working directory is "HDV-LIG14".
# - Ensure to have Java Install and to meet the requirement to run SPOT-RNA
# - Install Graph with the following command
#     $ brew install cpanminus && sudo cpanm Graph
# - Activate the python virtual environment for SPOT-RNA algorithm
#     $ conda activate venv
# - Copy the fasta folders "dataset_directory/fasta/single" and "dataset_directory/fasta/batch" to SPOT-RNA/sample_inputs

dir=$(pwd)

basedir="Dataset-Generator"

source ${dir}/${basedir}/color.sh
source ${dir}/${basedir}/validate_results.sh
source ${dir}/${basedir}/relocate.sh
source ${dir}/${basedir}/git_add.sh

# Assign default values when arguments are not provided
batch_size=$1 && [ -z "$1" ] && batch_size=1
starting_index=$2 && [ -z "$2" ] && starting_index=0
dataset_directory=$3 && [ -z "$3" ] && dataset_directory="Datasets/tmp"
ending_index=$4 && [ -z "$4" ] && ending_index=16383 # 16383
commit_size=$5 && [ -z "$5" ] && commit_size=50 # ~= 75 MB : Max push size: 100 MB

batch_count=$starting_index
# commit_counter=0 # count the number of 'commits' to be squashed

# create branch if it does not exist, and checkout to it.
branch_name="DatasetGenerator"
git checkout ${branch_name} 2>/dev/null || git checkout -b ${branch_name}
git push -u origin ${branch_name} # Publish branch

for name in $( eval echo {$starting_index..$ending_index} )
do
    # Will generate a complete batch using SPOT-RNA (Improve performance over generating individual fasta sequence)
    batch=$(($name % $batch_size))
    if (($batch == 0))
    then
        echo "${BOLD}Generating batch #${batch_count}${NC}"
        
        cd SPOT-RNA >/dev/null
        input_dir="sample_inputs/batch/size_${batch_size}/BATCH_SEQUENCE_${batch_count}.fasta"
        python3 SPOT-RNA.py --inputs ${input_dir} --outputs 'outputs/' --plots True --motifs True --cpu 128 # --gpu 0
        sleep 2
        cd - >/dev/null
        
        ((batch_count+=$batch_size))
    fi
    
    # Check for missing files and print them in white upon first try
    all_files_present "${dir}/SPOT-RNA/outputs" ${name}; retval=$?
    [ "$retval" -eq 1 ] && echo "${BOLD}${RED}SEQUENCE_${name} Failed to Completely Generate${NC}" # oneline if ... then ...
    IFS=""; printf "%s\n" ${retlog[@]} # IFS set the delimiter for printf

    # Will regenerate missing data using the individual fasta sequence and retry until SPOT-RNA successfully create the files
    until [ $retval -eq 0 ]
    do
        echo "${BOLD}${YELLOW}Trying To Resolve Missing Data${NC}"
        
        cd SPOT-RNA >/dev/null
        input_dir="sample_inputs/single/SEQUENCE_${name}.fasta"
        python3 SPOT-RNA.py --inputs ${input_dir} --outputs 'outputs/' --plots True --motifs True --cpu 128 # --gpu 0
        sleep 2
        cd - >/dev/null
        
        # Check for missing files and print them in red upon retry
        all_files_present "${dir}/SPOT-RNA/outputs" ${name}; retval=$?
        printf "${RED}%s\n${NC}" ${retlog[@]}
    done
    
    # Relocate Data to $dataset_directory
    echo "${GREEN}${MVUP}Relocating SEQUENCE_${name} to $dataset_directory${NC}"
    relocate_move "${dir}/SPOT-RNA/outputs/SEQUENCE_${name}" "$dataset_directory" # relocate_copy(...)
    sleep 1
    
    echo "${GREEN}${MVUP}${DEL}Adding SEQUENCE_${name}${NC}"
    git_add "${dataset_directory}" "SEQUENCE_${name}"
    echo "${GREEN}${BOLD}SEQUENCE_${name} Added!${NC}"
    
    commit_ready=$(($name % $commit_size))
    start=$(($name - $commit_ready))
    end=$name
    
    if (($commit_ready == commit_size-1)) || (($name == $ending_index))
    then
        echo "Commit Ready for SEQUENCE_${start}_to_${end}"
        git commit -m "SEQUENCE_${start}_To_${end}"
        git push
        # (( commit_counter++ ))
    fi
done

# Squash all change and push with lease for manual revision
git checkout main
git merge --squash ${branch_name}
git commit --no-edit
git push --force-with-lease

# More Git command:
# ref: https://www.bitdegree.org/learn/git-commit-command

# TODO:
# - Update and Test SPOT-RNA.py
# - Generate HDV and LIG data
