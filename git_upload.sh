
start=$1
end=$2

echo "Uploading SEQUENCE_${start}_To_${end}"

git commit -m "SEQUENCE_${start}_To_${end}"

git push


# More Git command:
# https://www.bitdegree.org/learn/git-commit-command
