
copy() {
    local src_file=$1
    local dest_path=$2
    mkdir -p ${dest_path} && cp ${src_file} ${dest_path}
}

relocate_copy() {
    local name=$1
    local src_path=$2 # source path
    local dest_path=$3 # destination path

    #src_path=${dir}/SPOT-RNA/outputs
    
    #dest_path=Datasets/HDV/
    #dest_path=Datasets/LIG/
    
    copy ${src_path}/SEQUENCE_${name}.st ${dest_path}/st
    copy ${src_path}/SEQUENCE_${name}.ct ${dest_path}/ct
    copy ${src_path}/SEQUENCE_${name}.dbn ${dest_path}/dbn
    copy ${src_path}/SEQUENCE_${name}.prob ${dest_path}/prob
    copy ${src_path}/SEQUENCE_${name}.bpseq ${dest_path}/bpseq
    copy ${src_path}/SEQUENCE_${name}_line.png ${dest_path}/line
    copy ${src_path}/SEQUENCE_${name}_radiate.png ${dest_path}/radiate

    # copy $dir/SPOT-RNA/sample_inputs/SEQUENCE_${name}.fasta $dir/fasta
}

relocate_move() {
    local name=$1
    local src_path=$2 # source path
    local dest_path=$3 # destination path

    #src_path=${dir}/SPOT-RNA/outputs
    
    #dest_path=Datasets/HDV/
    #dest_path=Datasets/LIG/
    
    mv ${src_path}/SEQUENCE_${name}.st ${dest_path}/st
    mv ${src_path}/SEQUENCE_${name}.ct ${dest_path}/ct
    mv ${src_path}/SEQUENCE_${name}.dbn ${dest_path}/dbn
    mv ${src_path}/SEQUENCE_${name}.prob ${dest_path}/prob
    mv ${src_path}/SEQUENCE_${name}.bpseq ${dest_path}/bpseq
    mv ${src_path}/SEQUENCE_${name}_line.png ${dest_path}/line
    mv ${src_path}/SEQUENCE_${name}_radiate.png ${dest_path}/radiate
}


