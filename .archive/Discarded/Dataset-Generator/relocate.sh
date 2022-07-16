
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

relocate_move() {
    local src_file=$1 # source filepath
    local dest_path=$2 # destination path

    #src_path=${dir}/SPOT-RNA/outputs
    
    #dest_path=Datasets/HDV/
    #dest_path=Datasets/LIG/
    
    mv ${src_file}.st ${dest_path}/st
    mv ${src_file}.ct ${dest_path}/ct
    mv ${src_file}.dbn ${dest_path}/dbn
    mv ${src_file}.prob ${dest_path}/prob
    mv ${src_file}.bpseq ${dest_path}/bpseq
    mv ${src_file}_line.png ${dest_path}/line
    mv ${src_file}_radiate.png ${dest_path}/radiate
}


