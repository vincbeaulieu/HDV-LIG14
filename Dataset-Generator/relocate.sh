
copy() {
    local src_file=$1 # source filepath
    local dest_path=$2 # destination path
    mkdir -p ${dest_path} && cp ${src_file} ${dest_path}
}

# relocate a copy of the source sequence files to destination path with subfolder arrangement
relocate_copy() {
    local src_file=$1 # source filepath
    local dest_path=$2 # destination path

    #src_file=${dir}/SPOT-RNA/outputs/SEQUENCE_${name}
    
    #dest_path=Datasets/HDV/
    #dest_path=Datasets/LIG/
    
    copy ${src_file}.st ${dest_path}/st
    copy ${src_file}.ct ${dest_path}/ct
    copy ${src_file}.dbn ${dest_path}/dbn
    copy ${src_file}.prob ${dest_path}/prob
    copy ${src_file}.bpseq ${dest_path}/bpseq
    copy ${src_file}_line.png ${dest_path}/line
    copy ${src_file}_radiate.png ${dest_path}/radiate

    # copy $dir/SPOT-RNA/sample_inputs/SEQUENCE_${name}.fasta $dir/fasta
}

move() {
    local src_file=$1 # source filepath
    local dest_path=$2 # destination path
    mkdir -p ${dest_path} && mv ${src_file} ${dest_path}
}

relocate_move() {
    local src_file=$1 # source filepath
    local dest_path=$2 # destination path

    #src_path=${dir}/SPOT-RNA/outputs

    #dest_path=Datasets/HDV/
    #dest_path=Datasets/LIG/
    
    move ${src_file}.st ${dest_path}/st
    move ${src_file}.ct ${dest_path}/ct
    move ${src_file}.dbn ${dest_path}/dbn
    move ${src_file}.prob ${dest_path}/prob
    move ${src_file}.bpseq ${dest_path}/bpseq
    move ${src_file}_line.png ${dest_path}/line
    move ${src_file}_radiate.png ${dest_path}/radiate
}


