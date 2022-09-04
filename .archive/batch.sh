
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
source ${dir}/${basedir}/all_files_present.sh
source ${dir}/${basedir}/relocate.sh
source ${dir}/${basedir}/git_add.sh

batch() {
    # This function use global variable from Dataset_Generator.sh
    local tmp_dir="sample_inputs/tmp_batch.fasta"
    local batch_count=$starting_index
    # commit_counter=0 # count the number of 'commits' to be squashed

    for name in $( eval echo {$starting_index..$ending_index} )
    do
        # Will generate a complete batch using SPOT-RNA (Improve performance over generating individual fasta sequence)
        local batch_ready=$(($name % $batch_size))
        if (($batch_ready == 0 && $batch_size > 0))
        then
            echo "${BOLD}Generating Batch #${batch_count}${NC}"
            
            cd SPOT-RNA >/dev/null
            input_dir="sample_inputs/batch/size_${batch_size}/BATCH_SEQUENCE_${batch_count}.fasta"
            python3 SPOT-RNA.py --inputs ${input_dir} --outputs 'outputs/' --plots True --motifs True --cpu ${nb_of_cpu} # --gpu 0
            sleep 2
            cd - >/dev/null

            last_name=$(($name + $batch_size))
            for index in $( eval echo {$name..$last_name} )
            do
                # Check for missing files and print them in white upon first try
                all_files_present "${dir}/SPOT-RNA/outputs" ${index}; retval=$? # from validate_results.sh
                [ "$retval" -eq 1 ] && echo "${BOLD}${YELLOW}SEQUENCE_${index} Failed to Completely Generate${NC}"
                IFS=""; printf "%s\n" ${retlog[@]} # IFS set the delimiter for printf

                if [ $retval -ne 0 ]
                then
                    cd SPOT-RNA >/dev/null
                    input_dir="sample_inputs/single/SEQUENCE_${index}.fasta"

                    # create tmp file or append the fasta sequence to it, if any files of that sequence are missing
                    cat $input_dir >> $tmp_dir
                    cd - >/dev/null
                fi
            done

            if [ -f "$tmp_dir" ] # if tmp.fasta exist:
            then
                echo "${BOLD}${YELLOW}Trying To Resolve Missing Data for Batch #${batch_count}${NC}"

                cd SPOT-RNA >/dev/null
                input_dir=$tmp_dir
                python3 SPOT-RNA.py --inputs ${input_dir} --outputs 'outputs/' --plots True --motifs True --cpu ${nb_of_cpu} # --gpu 0
                sleep 2
                cd - >/dev/null

                rm "SPOT-RNA/${tmp_dir}"
            fi

            ((batch_count+=$batch_size))
        fi


        # Check for missing files and print them in yellow upon second try
        all_files_present "${dir}/SPOT-RNA/outputs" ${name}; retval=$? # from validate_results.sh
        [ "$retval" -eq 1 ] && echo "${BOLD}${YELLOW}SEQUENCE_${name} Failed to Completely Generate${NC}"
        IFS=""; printf "%s\n" ${retlog[@]} # IFS set the delimiter for printf

        # Will regenerate missing data using the individual fasta sequence and retry until SPOT-RNA successfully create the files
        runtime=0 # In total, a sequence has 5 chances to generate all of its data
        until [ $retval -eq 0 ]
        do
            [ "$runtime" -gt 2 ] && exit 1 || (( runtime++ )) # Sequence failed to generate after 2 times - EXIT CODE 1
            
            echo "${BOLD}${YELLOW}Trying To Resolve Missing Data${NC}"
            
            cd SPOT-RNA >/dev/null
            input_dir="sample_inputs/single/SEQUENCE_${name}.fasta"
            python3 SPOT-RNA.py --inputs ${input_dir} --outputs 'outputs/' --plots True --motifs True --cpu ${nb_of_cpu} # --gpu 0
            sleep 2
            cd - >/dev/null
            
            # Check for missing files and print them in red upon retry
            all_files_present "${dir}/SPOT-RNA/outputs" ${name}; retval=$?
            printf "${RED}%s\n${NC}" ${retlog[@]}
        done
        
        # Relocate Data to $dataset_directory
        echo "${GREEN}${MVUP}Relocating SEQUENCE_${name} to $dataset_directory${NC}"
        relocate_move "${dir}/SPOT-RNA/outputs/SEQUENCE_${name}" "$dataset_directory" # relocate_copy
        sleep 0.1
        
        echo "${GREEN}${MVUP}${DEL}Adding SEQUENCE_${name}${NC}"
        git_add "${dataset_directory}" "SEQUENCE_${name}"
        echo "${GREEN}${BOLD}SEQUENCE_${name} Added!${NC}"
        
        commit_ready=$((($name - $starting_index) % $commit_size))
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
}
