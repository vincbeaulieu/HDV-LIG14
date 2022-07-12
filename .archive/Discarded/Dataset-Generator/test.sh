

























exit 0

# FLAG:
log_enabled=false


function DataGen () {

    batch_size=$1 && [ -z "$1" ] && batch_size=1
    starting_index=$2 && [ -z "$2" ] && starting_index=0
    ending_index=$4 && [ -z "$4" ] && ending_index=16383 # 16383
    dataset_directory=$3 && [ -z "$3" ] && dataset_directory="Datasets/tmp"
    
    commit_size=500
    nb_of_cpu=$(sysctl -n hw.physicalcpu_max)

    while test $# -gt 0;
    do
        case "$1" in
            -h|--help)
                echo "DataGen [batch_size] [stating_index] [dataset_directory] [ending_index] [commit_size]"
                echo " "
                echo "options:"
                echo "-h, --help            show brief help"
                echo "-l, --log             enable log files"
                echo "-c, --cpu             set a cpu limit"
                echo "-d, --output_dir      specify a directory to store generated outputs  - default: Datasets/tmp"
                echo "-cs, --commit_size    qte of sequences before performing a commit     - default: 500"
                echo "-r, --range           sequence range to generate                      - default: 0 to 16383"
                exit 0
                ;;
            -l|--log)
                log_enabled=true
                shift
                ;;
            -c|--cpu)
                nb_of_cpu=$2
                shift 2
                ;;
            -d|--output_dir)
                dataset_directory=$2
                shift 2
                ;;
            -cs|--commit_size)
                commit_size=$2
                shift 2
                ;;
            -r|--range)
                stating_index=$2
                ending_index=$3
                shift 3
                ;;
            
            *)
                echo "$1 : error : unrecognized flag"
                exit 1;
                ;;
        esac
    done
    
    echo "log_enabled : $log_enabled"
    echo "cpu_limit   : $nb_of_cpu"
    echo "output_dir  : $dataset_directory"
}

DataGen 100 0

exit 0




for name in $( eval echo {$starting_index..$ending_index} )
do
    #echo $name
    commit_ready=$((($name - $starting_index) % $commit_size))
    start=$(($name - $commit_ready))
    end=$name
    if (($commit_ready == commit_size-1)) || (($name == $ending_index))
    then
        echo "Commit Ready for SEQUENCE_${start}_to_${end}"
    fi
done

for MYFIELD in "$@"; do

        CHECKFIRST=`echo $MYFIELD | cut -c1`

        if [ "$CHECKFIRST" == "-" ]; then
            mode="flag"
        else
            mode="arg"
        fi

        if [ "$mode" == "flag" ]; then
            case $MYFIELD in
                -a)
                    CURRENTFLAG="VARIABLE_A"
                    ;;
                -b)
                    CURRENTFLAG="VARIABLE_B"
                    ;;
                -c)
                    CURRENTFLAG="VARIABLE_C"
                    ;;
            esac
        elif [ "$mode" == "arg" ]; then
            case $CURRENTFLAG in
                VARIABLE_A)
                    VARIABLE_A="$MYFIELD"
                    ;;
                VARIABLE_B)
                    VARIABLE_B="$MYFIELD"
                    ;;
                VARIABLE_C)
                    VARIABLE_C="$MYFIELD"
                    ;;
            esac
        fi
    done
