name=$1

git add \
ct/SEQUENCE_$name.ct \
dbn/SEQUENCE_$name.dbn \
line/SEQUENCE_${name}_line.png \
radiate/SEQUENCE_${name}_radiate.png \
prob/SEQUENCE_$name.prob \
bpseq/SEQUENCE_$name.bpseq \
st/SEQUENCE_$name.st \
fasta/SEQUENCE_$name.fasta

# Exception should be raise if any of these files are missing.
