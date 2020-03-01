#!/usr/bin/env python

import os
import h5py
import numpy as np
import statistics
import pickle
from hdf_filter_and_cleaning import *

directory = os.listdir()

#initialize a dictionary of summary stats
summary_stats = {}
sample_rate_files = {}
ten_channels=['ch_106','ch_110']
ten_channels_dict = {}
for i in ten_channels:
    ten_channels_dict[i] = 1

#script to get the average, min, and max of each file's channels into a single dictionary 
for file in directory:
    if file.endswith('.hdf'):

        #import file, get list of channels within file
        f = h5py.File(file,'r')
        chanIDs = f['DYNAMIC DATA']
        print(file)
        #add file to dictionary
        summary_stats[file]= {}

        for dataset in chanIDs:
            if dataset in ten_channels_dict:
                print(dataset)
                #initialize array of data points from a channel
                dset = chanIDs[dataset]['MEASURED']
                sample_rate_files[file] = get_sample_rate(file)[0]
     
                #create Dictionary Keys for average, min, max
                summary_stats[file][dataset]={}
                summary_stats[file][dataset]['min'] = {}
                summary_stats[file][dataset]['max'] = {}
     
                #clean array to get rid of underrepresented data points according to bins
                cleaned = get_bin_sizes(dset,4,0.05)
                
                #add min and max of filtered data to summary_stats
                summary_stats[file][dataset]['min'] = get_channel_min(cleaned)    
                print('min added')
                summary_stats[file][dataset]['max'] = get_channel_max(cleaned)
                print('max added')
        f.close()

print (summary_stats)
print(sample_rate_files)

final_filter = filter_channels_historic(summary_stats,2)


summary = open('filtered_summary.pkl', 'wb')
pickle.dump(final_filter, summary)
summary.close()         

sample_files = open('filtered_sample_rate.pkl', 'wb')
pickle.dump(sample_rate_files, sample_files)
sample_files.close()
