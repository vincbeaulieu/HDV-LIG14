
# COMMAND INFO:
# sh Dataset_Generator.sh [batch_size] [stating_index] [dataset_directory] [ending_index] [commit_size] [nb_of_cpu]

# Global variables: 
dir=$(pwd)
basedir="Dataset-Generator"

source ${dir}/${basedir}/batch.sh

# TODO: NOTE: Do your research before using the following command!
# create branch if it does not exist, and checkout to it.
# branch_name="DatasetGenerator"
# git checkout ${branch_name} 2>/dev/null || git checkout -b ${branch_name}
# git push -u origin ${branch_name} # Publish branch

batch_logger() {
    # batch $1 $2 $3 $4 $5 $6 # &> "${basedir}/log/${2}to${4}.log" &
    mkdir -p "${basedir}/log" # Create log directory if it doesn't exist
    batch $1 $2 $3 $4 $5 $6 2>&1 | tee -a "${basedir}/log/${2}to${4}.log"
}

if ( batch_logger $1 $2 $3 $4 $5 $6 ) # if command fail
then
    echo "\n-- ${YELLOW}Please ensure that the python virtual environment is activated and meet the requirements to run the SPOT-RNA algorithm. More information at: https://github.com/jaswindersingh2/SPOT-RNA${NC} --\n"
fi

# TODO: NOTE: commands below have --NOT-- been tested! Do your research before using them!
# Squash all change and push with lease for manual revision
# git checkout main
# git merge --squash ${branch_name}
# git commit --no-edit
# git push --force-with-lease

# More Git command:
# ref: https://www.bitdegree.org/learn/git-commit-command

