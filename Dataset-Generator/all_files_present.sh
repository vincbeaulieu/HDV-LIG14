

# source $(pwd)/SPOT-RNA/git/color.sh

all_files_present() {
    local path=$1
    local name=$2

    local seq_name="SEQUENCE_${name}"

    local ERROR=0

    retlog=() # global variable

    # printf "${RED}"
    [[ ! -f ${path}/${seq_name}.st ]] && retlog[0]="${seq_name}.st : MISSING" && ERROR=1
    [[ ! -f ${path}/${seq_name}.ct ]] && retlog[1]="${seq_name}.ct : MISSING" && ERROR=1
    [[ ! -f ${path}/${seq_name}.dbn ]] && retlog[2]="${seq_name}.dbn : MISSING" && ERROR=1
    [[ ! -f ${path}/${seq_name}.prob ]] && retlog[3]="${seq_name}.prob : MISSING" && ERROR=1
    [[ ! -f ${path}/${seq_name}.bpseq ]] && retlog[4]="${seq_name}.bpseq : MISSING" && ERROR=1
    [[ ! -f ${path}/${seq_name}_line.png ]] && retlog[5]="${seq_name}_line.png : MISSING" && ERROR=1
    [[ ! -f ${path}/${seq_name}_radiate.png ]] && retlog[6]="${seq_name}_radiate.png : MISSING" && ERROR=1
    # printf "${NC}"
    
    #echo ${RED}${retlog[@]}${NC}
    #for ((i=0; i < ${#retlog[@]}; i++ )); do echo "${retlog[$i]}"; done
    #printf "%s\n" ${retlog[@]}

    return ${ERROR}
}


