
cpu=$(sysctl -n hw.physicalcpu_max)
# sysctl -n hw.logicalcpu_max

echo $cpu

# ref: https://stackoverflow.com/questions/6481005/how-to-obtain-the-number-of-cpus-cores-in-linux-from-the-command-line

