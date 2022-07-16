source ${dir}/${basedir}/color.sh

git_add() {
    local dataset_dir=$1
    local seq_name=$2
    
    echo "${GREEN}${MVUP}${DEL}Adding ${seq_name}${NC}"
    
    printf "${NC}${RED}" # Print in red any files missing.
    git add \
    ${dataset_dir}/st/${seq_name}.st \
    ${dataset_dir}/ct/${seq_name}.ct \
    ${dataset_dir}/dbn/${seq_name}.dbn \
    ${dataset_dir}/prob/${seq_name}.prob \
    ${dataset_dir}/bpseq/${seq_name}.bpseq \
    ${dataset_dir}/line/${seq_name}_line.png \
    ${dataset_dir}/radiate/${seq_name}_radiate.png # \
    # ${dataset_dir}/fasta/${seq_name}.fasta
    printf "${NC}"
    
    echo "${GREEN}${BOLD}${seq_name} Added!${NC}"
}
