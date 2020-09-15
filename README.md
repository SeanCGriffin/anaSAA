# anaSAA

Contains scripts for use on SLAC computers to analyse Fermi-LAT LRS data.


Contents: 

### bulk_get_gps.py / get_gps.py 

Query the database using MnemRet.py to get Fermi GPS data. Dates can be specified as years, in which case Jan 1 is the default date. The 'delta' parameter is the number of days from the start period to query. 

### bulk_get_lrs.py / proc_lrs.py 

Get LRS data for CAL, TKR, or ACD. The bulk getter looks for GPS output files and gets the corresponding data. 
