#!/usr/bin/env python

import sys 
import os

if len(sys.argv) != 4:
    print("Usage: {0} <output> <YYYY-MM-DD> <delta_in_days>".format(sys.argv[0]))
    exit()


DATE = sys.argv[2]
DELTA = sys.argv[3]

OUTPUT_DIR= sys.argv[1]

OUTPUT_FILE="{0}/GPS_{1}_{2}.csv".format(OUTPUT_DIR, DATE, DELTA)

print("Pulling GPS info for {0} + {1} days and storing to: {2}".format(DATE, DELTA, OUTPUT_FILE))

command_str = "MnemRet.py -b '{0} 00:00:00' -e '+{1} day' --csv {2} SGPSBA_SECONDS SGPSBA_SUBSECS SGPSBA_POSITIONX SGPSBA_POSITIONY SGPSBA_POSITIONZ"

os.system(command_str.format(DATE, DELTA, OUTPUT_FILE))
