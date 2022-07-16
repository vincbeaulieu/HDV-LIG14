
# COMMAND INFO:
# source ${dir}/${basedir}/batch.sh
# batch [batch_size] [stating_index] [dataset_directory] [ending_index] [commit_size] [nb_of_cpu]

# Prior to executing the command:
# - Ensure that the terminal working directory is "HDV-LIG14".
# - Ensure to have Java Install and to meet the requirement to run SPOT-RNA
# - Install Graph with the following command
#     $ brew install cpanminus && sudo cpanm Graph
# - Activate the python virtual environment for SPOT-RNA algorithm
# - Copy the fasta folders "dataset_directory/fasta/single" and "dataset_directory/fasta/batch" to SPOT-RNA/sample_inputs

#dir=$(pwd)
#basedir="Dataset-Generator"

source ${dir}/${basedir}/color.sh
source ${dir}/${basedir}/generator.sh
source ${dir}/${basedir}/all_files_present.sh
source ${dir}/${basedir}/relocate.sh
source ${dir}/${basedir}/git_add.sh
source ${dir}/${basedir}/git_commit.sh

batch() {
    # Assign default values when arguments are not provided
    batch_size=$1 && [ -z "$1" ] && batch_size=1
    starting_index=$2 && [ -z "$2" ] && starting_index=0
    dataset_directory=$3 && [ -z "$3" ] && dataset_directory="Datasets/tmp"
    ending_index=$4 && [ -z "$4" ] && ending_index=16383 # 16383
    commit_size=$5 && [ -z "$5" ] && commit_size=500
    nb_of_cpu=$6 && [ -z "$6" ] && nb_of_cpu=$(sysctl -n hw.physicalcpu_max) # sysctl -n hw.logicalcpu_max
    # SPOT-RNA appears to be using physical cores instead of logical cores.

    local batch_count=$starting_index
    for name in $( eval echo {$starting_index..$ending_index} )
    do
        # Will generate a complete batch using SPOT-RNA (Improve performance over generating individual fasta sequence)
        local batch=$(($name % $batch_size))
        if (($batch == 0))
        then
            echo "${BOLD}Generating batch #${batch_count}${NC}"
            
            cd SPOT-RNA >/dev/null
            input_dir="sample_inputs/batch/size_${batch_size}/BATCH_SEQUENCE_${batch_count}.fasta"
            python3 SPOT-RNA.py --inputs ${input_dir} --outputs 'outputs/' --plots True --motifs True --cpu ${nb_of_cpu} # --gpu 0
            sleep 2
            cd - >/dev/null
            
            ((batch_count+=$batch_size))
        fi
        
        local sequence_name="SEQUENCE_${name}"
        
        # Check for missing files and print them in white upon first try
        all_files_present "${dir}/SPOT-RNA/outputs" ${sequence_name}; retval=$? # from validate_results.sh
        [ "$retval" -eq 1 ] && echo "${BOLD}${RED}${sequence_name} Failed to Completely Generate${NC}"
        IFS=""; printf "%s\n" ${retlog[@]} # IFS set the delimiter for printf

        # Will regenerate missing data using the individual fasta sequence and retry until SPOT-RNA successfully create the files
        local runtime=0
        until [ $retval -eq 0 ]
        do
            [ "$runtime" -gt 3 ] && exit 1 || (( runtime++ )) # Sequence failed to generate after 3 times - EXIT CODE 1
            
            echo "${BOLD}${YELLOW}Trying To Resolve Missing Data${NC}"
            
            cd SPOT-RNA >/dev/null
            input_dir="sample_inputs/single/${sequence_name}.fasta"
            python3 SPOT-RNA.py --inputs ${input_dir} --outputs 'outputs/' --plots True --motifs True --cpu ${nb_of_cpu} # --gpu 0
            sleep 2
            cd - >/dev/null
            
            # Check for missing files and print them in red upon retry
            all_files_present "${dir}/SPOT-RNA/outputs" ${name}; retval=$?
            printf "${RED}%s\n${NC}" ${retlog[@]}
        done
        
        # Relocate sequences to $dataset_directory
        echo "${GREEN}${MVUP}Relocating ${sequence_name} to $dataset_directory${NC}"
        relocate_move "${dir}/SPOT-RNA/outputs/${sequence_name}" "$dataset_directory" # relocate_copy
        sleep 0.5
        
        # Adding sequences for the next commit
        git_add "${dataset_directory}" "${sequence_name}"
        
        # if commit size is reach or last sequence has been generated, then commit.
        git_commit "${name}" "${starting_index}" "${ending_index}" "${commit_size}"
    done
}

