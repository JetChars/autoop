#!/bin/sh

# use ``cp`` ``truncate`` or move
# backup filename.1 to filename.2 and so forth
# compress backup file into gz files

# init
MODE=move
POS=1
COUNT=0
# du's minimum unit is kb, which represent actual disk useage
FILE_SIZE=`du FILENAME | awk '{print $1}'`

# gzip compress files to gz


# get opts
until [ $# -eq 0 ];do
    case $1 in
        -m | --mode)
            [[ $# < 2 ]] && break
            if [ $2 == move -o $2 == copytruncate ]; then
                echo MODE=$2
                shift
            else
                echo Wrong Argument
                break
            fi;;

        -h | --help | ?)
            echo "rotate_log.sh [-n] [-h|--help] [-z count]
            [-m|--mode copytruncate|move]
            [-s|-- size minsize] filename";;

        -n)
            echo 'do nothing'
            break;;
        -s)
            if [[ $2 =~ ^[0-9]+$ ]];then
                MIN_SIZE=$2
            elif [[ $2 =~ ^[0-9]+k$ ]]
                # min_size might contains more than one charactors
                MIN_SIZE=${2%%[K|M|G|k|m|g]}
                UNIT=${2:0-1}
                if [[ $UNIT == M -o $UNIT == m ]]; then
                    MIN_SIZE=$((MIN_SIZE*1024))
                elif [[ $UNIT == G -o $UNIT == g ]]
                    MIN_SIZE=$((MIN_SIZE*1024*1024))
                else
                    echo "wrong size"
                    exit(-1)
                fi
            else
                echo "error input"
            fi
            if [[ $FILE_SIZE < $MIN_SIZE ]]
                exit;;
            fi
        *)
            FILENAME=$1

    esac
    shift
done

# backup files
while [ -e $FILENAME.$POS ];do
    POS=$((POS+1))
done
while [[ $POS > 1 ]];do
    mv $FILENAME.$((POS-1)) $FILENAME.$POS
    POS=$((POS-1))
done
mv $FILENAME $FILENAME.1
touch $FILENAME
echo $POS

