#! /bin/bash

if [ $# -ne 3 ] ; then
    echo "Usage: $0 <output> <YYYYMMDD> <delta_in_days>"
    exit -1
fi

export DATE=$2
export DELTA=$3

export OUTPUT_DIR=$1

export OUTPUT_FILE="$OUTPUT_DIR/GPS_$DATE_$DELTA.csv"

echo "Pulling GPS info for $DATE + $DELTA days and storing to: $OUTPUT_FILE"

export COMMAND="MnemRet.py -b '$DATE 00:00:00' -e '+$DELTA day' --csv $OUTPUT_FILE SGPSBA_SECONDS SGPSBA_SUBSECS SGPSBA_POSITIONX SGPSBA_POSITIONY SGPSBA_POSITIONZ"
echo $COMMAND

$COMMAND