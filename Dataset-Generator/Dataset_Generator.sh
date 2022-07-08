
# COMMAND INFO:
# sh Dataset_Generator.sh [batch_size] [stating_index] [dataset_directory] [ending_index] [commit_size]

# Requirements:
# brew install parallel


dir=$(pwd)
basedir="Dataset-Generator"

source ${dir}/${basedir}/batch_copy.sh

# Assign default values when arguments are not provided
batch_size=$1 && [ -z "$1" ] && batch_size=1
starting_index=$2 && [ -z "$2" ] && starting_index=0
dataset_directory=$3 && [ -z "$3" ] && dataset_directory="Datasets/tmp"
ending_index=$4 && [ -z "$4" ] && ending_index=16383 # 16383
commit_size=$5 && [ -z "$5" ] && commit_size=50 # ~= 75 MB : Max push size: 100 MB

# TODO: Multithreading main function
# seq 1 100 | xargs -P 4 -I {} nohup batch {} &
# parallel -j 4 nohup batch ::: {1..100}
# ref: https://unix.stackexchange.com/questions/617994/how-to-limit-the-number-of-background-process-in-unix

# Squash all change and push with lease for manual revision
git checkout main
git merge --squash ${branch_name}
git commit --no-edit
git push --force-with-lease

# More Git command:
# ref: https://www.bitdegree.org/learn/git-commit-command

# TODO:
# - Generate HDV and LIG data
