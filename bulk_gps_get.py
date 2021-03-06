#!/usr/bin/env python

import os
import argparse
import time

from multiprocessing import Pool, Lock
from itertools import repeat

import subprocess

def run_scr_star(inputs):
    run_scr(*inputs)

def run_scr(year, delta, output):
    print(year)
    call_str = "./get_gps.py {0}/ {1} {2}".format(output, year, delta)
    print(call_str)
    subprocess.call(call_str, shell=True)
    
def main():


    print("Done!")
    return

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Load and merge TLL and TLRS data files.")

    #parser.add_argument("--start", type=str, help="")
    parser.add_argument("-j", "--jobs", type=int, help="Number of threads to spawn.")    
    parser.add_argument("-d", "--delta", type=int, help="Number of days from start to download.")
    parser.add_argument("-D", "--date", nargs='*', type=str, help="Date in YYYYMMDD format to download. If only YYYY specified, YYYY0101 will be used.")
    parser.add_argument("-o", "--output", type=str, help="Output directory")


    args = parser.parse_args()
    print(args) 

    if not args.jobs:
        print("Need to specify number of jobs.")
        exit()
    if not args.delta:
        print("Need to specify delta.")
        exit()
    if not args.date:
        print("Need to specify date(s)")
        exit()

    if not args.output:
        print("No output directory specified. Defaulting to local.")
        output_dir = './'
    else: 
        output_dir = args.output

    
    years = []
    for year in args.date:
        if len(year) == 4:
            years += [year + "-01-01"]
        else:
            year = year[0:4] + '-' + year[4:6] + '-' + year[6::]
            years += [year]

    print(years)


    pool = Pool(processes=args.jobs)
    pool.map(run_scr_star, zip(years, repeat(args.delta), repeat(output_dir)))

    print("Done. Exiting...")