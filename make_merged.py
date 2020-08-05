#!/usr/bin/env python


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


import time, sys
from IPython.display import clear_output

import argparse


def f(t_gps, t_unix):
    t_unix_mod = np.floor(t_unix % 60)

    if t_gps != t_unix_mod:

        delta = t_unix_mod - t_gps
        #print(delta)
        #print(t_unix)    
        if abs(delta) < 30:
            t_unix += -1 * delta
        elif abs(delta + 60) < 30:
            t_unix += (-1 * delta) - 60
        elif abs(delta - 60) < 30:
            t_unix += (-1 * delta) + 60
        else:
            print("GPS time differs by >60s from UNIX time.")
        
    return t_unix

def update_progress(progress):
    bar_length = 20
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
    if progress < 0:
        progress = 0
    if progress >= 1:
        progress = 1

    block = int(round(bar_length * progress))

    clear_output(wait = True)
    text = "Progress: [{0}] {1:.1f}%".format( "#" * block + "-" * (bar_length - block), progress * 100)
    print(text)

number_of_elements = 1000

#for i in range(number_of_elements):
    #time.sleep(0.00001) #Replace this with a real computation
#    update_progress(i / number_of_elements)

#update_progress(1)

def main(gps_file, tlrs_file, output=None):

    gps_df = pd.read_csv(gps_file)
    print(gps_df)
    sample = gps_df.loc[0::]

    x = sample.loc[:]['SGPSBA_POSITIONX']
    y = sample.loc[:]['SGPSBA_POSITIONY']
    z = sample.loc[:]['SGPSBA_POSITIONZ']

    lat = np.arctan2(z, np.sqrt(x**2 + y**2)) * 180. / np.pi
    lon = np.arctan2(y, x) * 180. / np.pi

    GPS_seconds = sample.loc[:]['SGPSBA_SECONDS']
    #Get MET and add subsections seconds
    UNIX_t = np.floor(sample.loc[:]['TSTAMP']-978307200)
    UNIX_t += sample.loc[:]['SGPSBA_SUBSECS']

    # Generate new data frame for time, lat, lon.
    tll_df = pd.DataFrame(data={'time': np.array([f(t_gps, t_unix) for t_gps, t_unix in zip(GPS_seconds, UNIX_t)]), 
                                  'lat':lat, 
                                  'lon':lon
                                 }
                          )

    print(f"Loaded TLL datafile {gps_file}.")
    l_orig = len(tll_df)
    tll_df.drop_duplicates(subset='time', inplace=True)
    l_new = len(tll_df)
    print(f"File contains {l_orig} entries and {l_new} non-duplicates.")
    print("Done.")


    # In[10]:


    # Last term drops the NaN at the end of the frame. 
    tlrs_df = pd.read_csv(tlrs_file, header=None, delimiter=' ').iloc[:,0:-1] 
    # Set column names. 
    tlrs_df.columns = ['time' if x==0 else x-1 for x in tlrs_df.columns]
    print(f"LRS data loaded. Number events: {len(tlrs_df)}")
    print(len(tlrs_df))
    tlrs_df.drop_duplicates(subset='time', inplace=True)
    print(f"LRS duplicates dropped. Remaining events: {len(tlrs_df)}")
    print(len(tlrs_df))
    tlrs_sorted_df = tlrs_df.sort_values('time')
    print("LRS sorted.")
    print("Done.")


    merged = pd.merge(tll_df, tlrs_df, 
                      left_on=tll_df['time'].astype(int), 
                      right_on=tlrs_df['time'].astype(int), suffixes=['_tll', '_tlrs'],
                      how='inner', copy=False)

    print(f"Merge complete.")
    print(len(merged))
    merged.drop_duplicates(subset=['time_tll', 'time_tlrs'], inplace=True)
    print(len(merged))


    if output is None:
        merged.to_csv('merged.csv')
    else:
        merged.to_csv(output)


    return

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Load and merge TLL and TLRS data files.")

    parser.add_argument("--gps", type=str, help="gps data file.")
    parser.add_argument("--tlrs", type=str, help="TLRS data file.")
    parser.add_argument("--output", type=str, help="Output filename." )    

    args = parser.parse_args()
    print(args)



    main(args.gps, args.tlrs, args.output)