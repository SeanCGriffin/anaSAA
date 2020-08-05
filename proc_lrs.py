#!/usr/bin/env python

import numpy as np
import pandas as pd

import argparse

def main(lrs_file, output=None):

    with open(lrs_file, 'r') as f:
        file_list = f.readlines()
        file_list = [l.rstrip() for l in file_list]
    

    df = pd.DataFrame()
    t0 = None

    i = 0
    nfiles_done = 0
    lrs_list = []

    for index,file in enumerate(file_list):
        print(f"Processing {file}. Progess {index+1}/{len(file_list)}.")
        with open(file) as f:
            for line in f:
                #Capture the line and turn it into an array.
                l = line.strip().split(',')
                #Check if timestamp or other:
                if len(l) == 1 and '.' in l[0]:
                    #We're at a timestamp (second clause is to catch the 0th entry)
                    #Verify this isn't the first event. 
                    if t0 is not None: 
                        #Set up the dataframe...
                        df = df.append([[float(t0)] + lrs_list], ignore_index=True)
                        lrs_list = []

                    t0 = l[0]

                elif len(l) == 4:
                    a = int(l[1])
                    b = int(l[2])
                    lrs_list += [a, b]
                else:
                    continue

    df.columns=["time_lrs"] + [f'ch{i:02d}' for i in range(len(df.columns)-1)]            
    df.info()    

    if output is None:
        df.to_csv('raw.csv', sep=',', index=False)
    else:
        df.to_csv(output, sep=',', index=False)

    return

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Load and merge TLL and TLRS data files.")

    parser.add_argument("--lrs", type=str, help="TLRS data file.")
    parser.add_argument("--output", type=str, help="Output filename." )    

    args = parser.parse_args()
    print(args)

    if not args.lrs:
        print("LRS data filename required!")
        exit()

    main(args.lrs, args.output)