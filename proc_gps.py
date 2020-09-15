#!/usr/bin/env python

import numpy as np
import pandas as pd
import os
import argparse

def fix_time(t_gps, t_unix):
    t_unix_mod = np.floor(t_unix % 60)

    if t_gps != t_unix_mod:

        delta = t_unix_mod - t_gps
        #print(delta)
        #print(t_unix)    
        if abs(delta) < 30.:
            t_unix += -1 * delta
        elif abs(delta + 60.) < 30.:
            t_unix += (-1. * delta) - 60.
        elif abs(delta - 60.) < 30.:
            t_unix += (-1. * delta) + 60.
        else:
            print("GPS time differs by >60s from UNIX time.")
            return None
        
    return t_unix

def process_runlist(file_list, output=None, write_csv=False, n_ana = -1):
    
    for index, gps_file in enumerate(file_list):
        print(f"Processing {gps_file}. Progess {index+1}/{len(file_list)}.")

        date = gps_file.split("_")
        year, month = [date[1].split('-')[0], date[1].split('-')[1]]
        print(gps_file, year, month)

        if n_ana < 0:
            gps_df = pd.read_csv(gps_file)
        else:
            gps_df = pd.read_csv(gps_file, nrows=n_ana)
            
        gps_df.info()
       
        sample = gps_df

        # Do math to get lat/lon
        x = sample.loc[:]['SGPSBA_POSITIONX']
        y = sample.loc[:]['SGPSBA_POSITIONY']
        z = sample.loc[:]['SGPSBA_POSITIONZ']

        lat = np.arctan2(z, np.sqrt(x**2. + y**2.)) * 180. / np.pi
        lon = np.arctan2(y, x) * 180. / np.pi

        GPS_seconds = sample.loc[:]['SGPSBA_SECONDS']
        #Get MET and add subsections seconds
        UNIX_t = np.floor(sample.loc[:]['TSTAMP']-978307200)
        UNIX_t += sample.loc[:]['SGPSBA_SUBSECS']

        # Generate new data frame for time, lat, lon.
        
        tll_df = pd.DataFrame(data={'time_tll': np.array([fix_time(t_gps, t_unix) for t_gps, t_unix in zip(GPS_seconds, UNIX_t)]), 
                                      'lat':lat, 
                                      'lon':lon
                                     }
                              )
        print(f"Done...")
        
        if write_csv:
            print(f"Writing GPS TLL data to {output}/GPS_{year}_{month}.csv")
            with open(f"{output}/GPS_{year}_{month}.csv", 'w') as f:
                tll_df.to_csv(f, index=False, sep=',')          
            #df.to_csv(f, header=f.tell()==0, index=False, sep=',')
        else:
            print(f"Writing GPS TLL data to {output}/GPS_{year}_{month}.h5")
            tll_df.to_hdf(f"{output}/GPS_{year}_{month}.h5", "tll", mode="w")          

    print("Done!")
    return

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Read GPS files ")

    parser.add_argument("-r", "--runlist", type=str, help="Runlist containing multiple GPS files. ")
    parser.add_argument("-g", "--gps", type=str, help="Path to file containing GPS data.")
    parser.add_argument("-o", "--output", type=str, help="Output directory (without suffix)." )
    parser.add_argument("-s", "--short", type=int, help="(Optional) Number of lins in GPS file to analyse." )    
    parser.add_argument("-c", "--csv", default=False, action='store_true', help="Output data to CSV rather than .h5")
    

    args = parser.parse_args()
    print(args)

    if not args.gps and not args.runlist:
        print("GPS file or runlist is required!")
        exit()
        
    if not args.output: 
        output = "./"
    else:
        output = args.output

    if args.gps:
        runlist = [args.gps]
    else:
        with open(args.runlist, 'r') as f:
            file_list = f.readlines()
            runlist = [l.rstrip() for l in file_list]
            
    if args.short:
        n_ana = args.short
    else:
        n_ana = -1
    
    print("Files to analyse:")
    for f in runlist:
        print(f"\t\t{f}")
        
    print("Short analysis? {0:s}".format(f"True! {n_ana}" if n_ana != -1 else "Nope."))

    
    process_runlist(runlist, output, args.csv, n_ana)
