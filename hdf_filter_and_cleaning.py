#!/usr/bin/env python

import os
import h5py
import numpy as np
import statistics
import pickle

def get_sample_rate(file):
    #Get sample rate of a machine
    #input: hdf file
    #output: list of sample rates in file
    f = h5py.File(file, 'r')

    chanIDs = f['DYNAMIC DATA']
    
    sample_rates = []

    for dataset in chanIDs:
        dataset = chanIDs[dataset]
        dataset_attrs = dataset.attrs
        sample_rates.append(dataset_attrs['SAMPLE RATE'])

    return (sample_rates)

def total_data_points(file):
    #get total data points in file
    #input: hdf file
    #output: list of total data points of each channel in file
    f = h5py.File(file, 'r')

    chanIDs = f['DYNAMIC DATA']
    
    number_data_points = []

    for dataset in chanIDs:
        dset = chanIDs[dataset]['MEASURED']
        measured = (dset[0:len(dset)])
        number_data_points.append(len(measured))

    return (number_data_points)

def total_channel(file):
    #get total channels of a hdf file
    #input: hdf file
    #output: list of total channels in a file
    f = h5py.File(file,'r')
    
    chanIDs = f['DYNAMIC DATA'] 
    return (len(chanIDs))

    
def get_channel_average(dataset):
    #get average measurement of a channel
    #input: channel column dataset
    #output: average of the column
    measured = dataset[0:len(dataset)]
    cleanedList = [x for x in measured if str(measured) != np.nan]
    return (np.nanmean(cleanedList))

def get_channel_min(dataset):
    #get min of channel
    #input: channel column dataset
    #output: min of column
    return (np.min(dataset[0:len(dataset)]))

def get_channel_max(dataset):
    #get max of channel
    #input:channel column dataset
    #output: max of column
    return (np.max(dataset[0:len(dataset)]))

def get_bin_sizes(dset,num_bins,percent_threshold):
    #uses bins to remove datapoints in a channel that are in underrepresented bins
    #INPUT 1: dset, an array of integers
    #INPUT 2: num_bins, number of bins to split dset across
    #INPUT 3: threshold, minimum percent of data points in a bin
    #         to avoid filtration
    #output: array of integers where datapoints in underrepresented bins are replaced by 'nan'
    bin_dist = np.histogram(dset,num_bins)
    bin_sizes = bin_dist[0]
    #check for variance in the datapoints
    if (bin_dist[1][-1] - bin_dist[1][0]) > 0:
        bin_offset = (bin_dist[1][-1] - bin_dist[1][0]) / (num_bins - 1)
        num_threshold  = len(dset) * percent_threshold
        cull_between = {}
        good_dset = []
        #add bins which fail the theshold requirement
        for i in range(len(bin_sizes)):
            if bin_sizes[i] < num_threshold:
                cull_between[i] = 1
        for entry in dset:
            entry_bin = int((entry - bin_dist[1][0]) / bin_offset)
            #filter out the variants.
            if entry_bin in cull_between:
                good_dset.append(np.nan)
            else:
                good_dset.append(entry)
        return good_dset
    else:
        return dset

def filter_channels_historic(in_dict,stdev_cutoff):
    #get global distribution of summary stats for each channel
    global_min = {}
    global_max = {}
    for key_file in in_dict:
        for key_channel in in_dict[key_file]:
            if key_channel not in global_min:
                global_min[key_channel] = []
                global_max[key_channel] = []

            global_min[key_channel].append(in_dict[key_file][key_channel]['min'])
            global_max[key_channel].append(in_dict[key_file][key_channel]['max'])

    #process global_min
    global_min_upper = {}
    global_min_lower = {}
    global_max_upper = {}
    global_max_lower = {}
    for key in global_min:
        
        global_min_mean = np.average(np.array(list(global_min.values()),dtype=np.float))
        global_min_stdev = np.std(np.array(list(global_min.values()),dtype=np.float))
        global_min_upper[key] = global_min_mean + (global_min_stdev * stdev_cutoff)
        global_min_lower[key] = global_min_mean - (global_min_stdev * stdev_cutoff)
    
        #process global_max
        global_max_mean = np.average(np.array(list(global_max.values()),dtype=np.float))
        global_max_stdev = np.std(np.array(list(global_max.values()),dtype=np.float))
        global_max_upper[key] = global_max_mean + (global_max_stdev * stdev_cutoff)
        global_max_lower[key] = global_max_mean - (global_max_stdev * stdev_cutoff)
    
    for key_file in in_dict:
        for key_channel in in_dict[key_file]:
            if in_dict[key_file][key_channel]['min'] > global_min_upper[key_channel]:
                del in_dict[key_file][key_channel]
            elif in_dict[key_file][key_channel]['min'] < global_min_lower[key_channel]:
                del in_dict[key_file][key_channel]
            if in_dict[key_file][key_channel]['max'] > global_max_upper[key_channel]:
                del in_dict[key_file][key_channel]
            elif in_dict[key_file][key_channel]['max'] < global_max_lower[key_channel]:
                del in_dict[key_file][key_channel]
    return in_dict


