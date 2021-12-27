
name=$1
dir=$(pwd)

mv $dir/SPOT-RNA/outputs/SEQUENCE_${name}_line.png $dir/line
mv $dir/SPOT-RNA/outputs/SEQUENCE_${name}_radiate.png $dir/radiate
mv $dir/SPOT-RNA/outputs/SEQUENCE_${name}.st $dir/st
mv $dir/SPOT-RNA/outputs/SEQUENCE_${name}.ct $dir/ct
mv $dir/SPOT-RNA/outputs/SEQUENCE_${name}.bpseq $dir/bpseq
mv $dir/SPOT-RNA/outputs/SEQUENCE_${name}.prob $dir/prob
mv $dir/SPOT-RNA/outputs/SEQUENCE_${name}.dbn $dir/dbn

cp $dir/SPOT-RNA/sample_inputs/SEQUENCE_${name}.fasta $dir/fasta