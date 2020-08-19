#! /bin/bash

if [ $# -ne 3 ] ; then
    echo "Usage: $0 <TKR|CAL|ACD> YYYY MM"
    exit -1
fi

ls -1 /nfs/farm/g/glast/u42/ISOC-flight/FswDumps/reports/nonEvent/$2/$3/*$1LRS/*.csv