
batch_size=$1 && [ -z "$1" ] && batch_size=1
starting_index=$2 && [ -z "$2" ] && starting_index=0
dataset_directory=$3 && [ -z "$3" ] && dataset_directory="Datasets/tmp"
ending_index=$4 && [ -z "$4" ] && ending_index=16383 # 16383
commit_size=$5 && [ -z "$5" ] && commit_size=500
nb_of_cpu=$6 && [ -z "$6" ] && nb_of_cpu=$(sysctl -n hw.physicalcpu_max)

for name in $( eval echo {$starting_index..$ending_index} )
do
    #echo $name
    commit_ready=$((($name - $starting_index) % $commit_size))
    start=$(($name - $commit_ready))
    end=$name
    if (($commit_ready == commit_size-1)) || (($name == $ending_index))
    then
        echo "Commit Ready for SEQUENCE_${start}_to_${end}"
    fi
done
