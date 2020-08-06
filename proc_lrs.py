#!/usr/bin/env python

import numpy as np
import pandas as pd
import os
import argparse

def main(lrs_file, output=None):

    if output is None:

        output = 'raw.csv'
        print(f"No output file specified; writing to {output}.")
        if os.path.exists(output):
            print(f"Default output file exists, deleting...")
            os.remove(output)    

    with open(lrs_file, 'r') as f:
        file_list = f.readlines()
        file_list = [l.rstrip() for l in file_list]
    
    ch_index = 0
    n_ch = None

    i = 0
    nfiles_done = 0
    lrs_list = []

    for index,file in enumerate(file_list):
        print(f"Processing {file}. Progess {index+1}/{len(file_list)}.")
        with open(file) as f:
            arr_index = -1
            lines = f.readlines()
            t_arr = np.zeros((len(lines)), dtype=float) - 999
            lrs_arr = np.zeros((len(lines), 100,), dtype=int) - 999
            for line in lines:
                #Capture the line and turn it into a list.
                
                l = line.strip().split(',')
                #Check if timestamp or other:
                if len(l) == 1 and '.' in l[0]:
                    arr_index += 1
                    t_arr[arr_index] = l[0]                
                    ch_index = 0
                    
                    #This bit figures out how many channels there are.
                    if arr_index == 1:
                        for i,val in enumerate(lrs_arr[0]):
                            if val == -999:
                                n_ch = i
                                print(f"Detected number of channels in dataset: {n_ch}")
                                break                
                    
                elif len(l) == 4:
                    lrs_arr[arr_index][ch_index] = int(l[1])
                    lrs_arr[arr_index][ch_index+1] = int(l[2])
                    
                    ch_index += 2
                else:
                    continue
            
            t_arr = t_arr[0:arr_index+1]
            lrs_arr = lrs_arr[0:arr_index+1, 0:n_ch]
            
            print(len(t_arr))
            
            t_df = pd.DataFrame(t_arr)
            lrs_df = pd.DataFrame(lrs_arr)
            df = pd.concat([t_df, lrs_df], axis=1)        
            
            with open(output, 'a') as f:
                
                df.columns=["time_lrs"] + [f'ch{i:02d}' for i in range(len(df.columns)-1)]
                #Write to disk, do not write header if the file is being created
                df.to_csv(f, header=f.tell()==0, index=False, sep=',')
                print(f"Outputting dataframe to {output}...")  

    print("Done!")
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

    if args.output:
        if os.path.exists(args.output):
            print(f"Output file {args.output} exists. Please remove before continuing with this filename.")
            exit()


    main(args.lrs, args.output)