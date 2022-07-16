source ${dir}/${basedir}/color.sh

# global variable
batch_count=$starting_index

batch_generator() {
    local name=$1
    local batch_size=$2
    local nb_of_cpu=$3

    # Generate sequences using the fasta batch files
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
}

single_generator() {
    local seq_name=$1

    # Check for missing files and print them in white upon first try
    all_files_present "${dir}/SPOT-RNA/outputs" ${seq_name}; retval=$? # from validate_results.sh
    [ "$retval" -eq 1 ] && echo "${BOLD}${RED}${seq_name} Failed to Completely Generate${NC}"
    IFS=""; printf "%s\n" ${retlog[@]} # IFS set the delimiter for printf
    
    # Will regenerate the missing data using the individual fasta sequence
    runtime=0
    until [ $retval -eq 0 ]
    do
        # if sequence failed to generate after 3 times then EXIT CODE 1
        [ "$runtime" -gt 3 ] && exit 1 || (( runtime++ ))
        
        echo "${BOLD}${YELLOW}Trying To Resolve Missing Data${NC}"
        
        cd SPOT-RNA >/dev/null
        input_dir="sample_inputs/single/${seq_name}.fasta"
        python3 SPOT-RNA.py --inputs ${input_dir} --outputs 'outputs/' --plots True --motifs True --cpu ${nb_of_cpu} # --gpu 0
        sleep 2
        cd - >/dev/null
        
        # Check for missing files and print them in red upon retry
        all_files_present "${dir}/SPOT-RNA/outputs" ${name}; retval=$?
        printf "${RED}%s\n${NC}" ${retlog[@]}
    done
}

