#!/bin/sh

rotate()
{
    if [ $1 = "copytruncate" ]; then
        copy $2 $3
        truncate -s 0 $2
    elif [ $1 = "move" ]; then
        mv -f $2 $3
        touch $2
    else
        echo "wrong mode"
        exit 1
    fi
}


# init
# ====
MODE=move
POS=1
GZ_CNT=0
MIN_SIZE=0

# get opts
# ========
until [ $# -eq 0 ];do
    case $1 in
        -h | --help | ?)
            echo "rotate_log.sh [-n] [-h|--help] [-z count]
            [-m|--mode copytruncate|move]
            [-s|-- size minsize] filename"
            ;;
        -m | --mode)
            [[ $# < 2 ]] && break
            if [ $2 == "move" -o $2 == "copytruncate" ]; then
                shift
            else
                echo "Wrong mode"
                exit 1
            fi 
            ;;
        -n)
            echo 'do nothing'
            exit
            ;;
        -s)
            if [[ $2 =~ ^[0-9]+$ ]];then
                MIN_SIZE=$2
            elif [[ $2 =~ ^[0-9]+[a-zA-Z]$ ]];then
                # min_size might contains more than one charactors
                MIN_SIZE=${2%%[K|M|G|k|m|g]}
                UNIT=${2:0-1}
                if [ $UNIT == "M" -o $UNIT == "m" ]; then
                    MIN_SIZE=$((MIN_SIZE*1024))
                elif [ $UNIT == "G" -o $UNIT == "g" ]; then
                    MIN_SIZE=$((MIN_SIZE*1024*1024))
                elif [ $UNIT == "K" -o $UNIT == "k" ]; then
                    MIN_SIZE=$2
                fi
            else
                echo "wrong input format"
                exit 1
            fi
            shift
            ;;
        -z)
            GZ_CNT=$2
            shift
            ;;
        *)
            FILENAME=$1
            if [ -e $FILENAME ];then
                FILE_SIZE=`du $FILENAME | awk '{print $1}'`
            else
                print "file does not exist!"
                exit 1
            fi
            ;;
    esac
    shift
done


# test filezise
# ==============
if [ $FILE_SIZE -lt $MIN_SIZE ];then
    exit 0
fi

# backup files
# ============
while [ -e $FILENAME.$POS ];do
    POS=$((POS+1))
done

if [ $GZ_CNT -eq 0 ];then
    GZ_CNT=$POS
fi

while [ $POS -gt 1 ];do
    rotate $MODE $FILENAME.$((POS-1)) $FILENAME.$POS
    if [ -e $FILENAME.$((POS-1)).gz ]; then
        rotate $MODE $FILENAME.$((POS-1)).gz $FILENAME.$POS.gz
    elif [ $POS -ge $GZ_CNT ]; then 
        gzip -c $FILENAME.$POS > $FILENAME.$POS.gz
    fi
    POS=$((POS-1))
done
rotate $MODE $FILENAME $FILENAME.1

