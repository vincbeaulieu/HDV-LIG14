
# COMMAND INFO:
# sh Dataset_Generator.sh [batch_size] [stating_index] [dataset_directory] [ending_index] [commit_size]

# Requirements:
# brew install parallel


dir=$(pwd)
basedir="Dataset-Generator"

source ${dir}/${basedir}/batch_copy.sh

# create branch if it does not exist, and checkout to it.
branch_name="DatasetGenerator"
git checkout ${branch_name} 2>/dev/null || git checkout -b ${branch_name}
git push -u origin ${branch_name} # Publish branch

# Assign default values when arguments are not provided
batch_size=$1 && [ -z "$1" ] && batch_size=1
starting_index=$2 && [ -z "$2" ] && starting_index=0
dataset_directory=$3 && [ -z "$3" ] && dataset_directory="Datasets/tmp"
ending_index=$4 && [ -z "$4" ] && ending_index=16383 #16383
commit_size=$5 && [ -z "$5" ] && commit_size=50 # ~= 75 MB : Max push size: 100 MB

batch_func() {
    # batch $1 $2 $3 $4 $5 # &> "log/${2}to${4}.log" &
    batch $1 $2 $3 $4 $5 2>&1 | tee -a "log/${2}to${4}.log"
}

N=2 # nb of python process
for name in $(seq $starting_index $batch_size $ending_index)
do
    ((i=i%N)); ((i++==0)) && wait
    
    let end_index=$name+$batch_size-1
    [ $end_index -gt $ending_index ] && end_index=$ending_index
    start_index=$name
   
    batch_func $batch_size $start_index $dataset_directory $end_index $commit_size
done

# Spot RNA appears to be using physical cores instead of logical cores. Therefore, multithreading the shell script won't resolve the performance issue.


# Squash all change and push with lease for manual revision
# git checkout main
# git merge --squash ${branch_name}
# git commit --no-edit
# git push --force-with-lease

# More Git command:
# ref: https://www.bitdegree.org/learn/git-commit-command

# TODO:
# - Generate HDV and LIG data
