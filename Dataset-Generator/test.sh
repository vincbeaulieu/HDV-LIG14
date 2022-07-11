

#for name in $( eval echo {$1..$2} ); do echo "$name"; done
#for name in $(seq $1 $2); do echo "$name"; done
#for i in $(seq 0 2 10); do echo $i; done
# for ((name=$1; name<=$2; name+=5)); do echo $name; done

batch_size=$1 && [ -z "$1" ] && batch_size=1
starting_index=$2 && [ -z "$2" ] && starting_index=0
dataset_directory=$3 && [ -z "$3" ] && dataset_directory="Datasets/tmp"
ending_index=$4 && [ -z "$4" ] && ending_index=643 # 16383
commit_size=$5 && [ -z "$5" ] && commit_size=50 # ~= 75 MB : Max push size: 100 MB

batch_func() {
    batch $1 $2 $3 $4 $5 > "${dir}/${basedir}/output.log" 2>&1 &
}

N=4
for (( name=$starting_index; name<=$ending_index; name+=$batch_size ))
do
    ((i=i%N)); ((i++==0)) && wait
    
    let end_index=$name+$batch_size
    [ $end_index -gt $ending_index ] && end_index=$ending_index
    start_index=$name
   
    batch_func $batch_size $start_index $dataset_directory $end_index $commit_size &
done



#for i in  ; do
 # echo $i
  #sem -j+0 echo $i ";" echo done
#done
#sem --wait
