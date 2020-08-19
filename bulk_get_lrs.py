#!/usr/bin/env python

import os
import argparse
import time

from multiprocessing import Pool, Lock
from itertools import repeat

import subprocess

import glob

import proc_lrs as plrs

def run_scr_star(inputs):
    run_scr(*inputs)

def run_scr(output_dir, subsystem, year_month, listonly):
    year = year_month[0]
    month = year_month[1]
    #print(year, month)

    target_file = "{0}/{1}LRS_{2}_{3}.list".format(output_dir, subsystem, year, month)
    call_str = "./make_filelist.sh {0} {1} {2} > {3}".format(subsystem, year, month, target_file)

    print(call_str)

    subprocess.call(call_str, shell=True)

    if not listonly:
        plrs.process_runlist(target_file, output=output_dir)
    
def main():


    print("Done!")
    return

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Locate and process LRS files.")

    #parser.add_argument("--start", type=str, help="")
    parser.add_argument("-j", "--jobs", type=int, default=1, help="Number of threads to spawn.")    
    parser.add_argument("-i", "--input", type=str, default="./analysis/GPS*.csv", help="Input directory in which to search for GPS files. All GPS files will have LRS data processed.")
    parser.add_argument("-o", "--output", type=str, default="./lrs/", help="Output directory")
    parser.add_argument("-s", "--subsystem", type=str, default="CAL", help="Subsystem: TKR, CAL, ACD")
    parser.add_argument("-l", "--listonly", type=bool, default=True, help="Generate filelists only.")

    args = parser.parse_args()
    print(args) 

    if not args.jobs:
        print("Need to specify number of jobs.")
        exit()
    if not args.subsystem:
        print("Subsystem not specified.")
        exit()
    elif args.subsystem not in ['TKR', 'CAL', 'ACD']:
        print("Unknown subsystem specified.")
        exit()


    if not args.output:
        print("No output directory specified. Defaulting to local.")
        output_dir = './'
    else: 
        output_dir = args.output

    year_month = []
    if not args.input:
        print("No input directory specified.")
        exit()
    else:
        GPS_files = sorted(glob.glob(args.input+"*.csv"))
        if len(GPS_files) == 0:
            print("NO GPS files found in directory. Exiting...")
        else:
            print("{0} files found in input directory:".format(len(GPS_files)))
            for f in GPS_files: 
                print(f)
                date = f.split("/")[-1].split("_")[1]
                print(date)
                year, month, day = date.split('-')
                year_month += [(year, month)]

    

    pool = Pool(processes=args.jobs)
    #pool.map(run_scr_star, zip(repeat(output_dir), repeat(args.delta), repeat(output_dir)))
    pool.map(run_scr_star, zip(repeat(output_dir), repeat(args.subsystem), year_month, repeat(args.listonly)))

    print("Done. Exiting...")
