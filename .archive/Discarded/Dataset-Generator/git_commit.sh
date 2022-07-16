
# global variables:
# commit_counter=0 # count the number of 'commits' to be squashed

git_commit() {
    # input arguments: [name] [starting_index] [ending_index] [commit_size]
    local name=$1
    local starting_index=$2
    local ending_index=$3
    local commit_size=$4
    
    local commit_ready=$((($name - $starting_index) % $commit_size))
    local start=$(($name - $commit_ready))
    local end=$name
    
    # if commit size is reach or last sequence has been generated, then commit.
    if (($commit_ready == commit_size-1)) || (($name == $ending_index))
    then
        echo "Commit Ready for SEQUENCE_${start}_to_${end}"
        git commit -m "SEQUENCE_${start}_To_${end}"
        git push
        # (( commit_counter++ ))
    fi
}
