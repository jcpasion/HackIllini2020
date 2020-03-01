#!/usr/bin/env python

import os
import h5py
import numpy as np
import statistics
import pickle

directory = os.listdir()

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
    #input: dset as an array of integers, number of bins, threshold
    #output: array of integers where datapoints in underrepresented bins are replaced by np.nan
    bin_dist = np.histogram(dset,num_bins)
    bin_sizes = bin_dist[0]
    if (bin_dist[1][-1] - bin_dist[1][0]) > 0:
        bin_offset = (bin_dist[1][-1] - bin_dist[1][0]) / (num_bins - 1)
        num_threshold  = len(dset) * percent_threshold
        cull_between = {}
        good_dset = []
        #add bins to cull
        for i in range(len(bin_sizes)):
            if bin_sizes[i] < num_threshold:
                cull_between[i] = 1
        for entry in dset:
            entry_bin = int((entry - bin_dist[1][0]) / bin_offset)
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




#initialize a dictionary of summary stats
summary_stats = {}
sample_rate_files = {}
ten_channels=['ch_1','ch_10','ch_100','ch_101','ch_102','ch_106','ch_107','ch_109','ch_11','ch_110']
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

        for dataset in ten_channels:
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

    
#         total_channels.append((total_channel(file)))
#        x = list(set(get_sample_rate(file)))
#        sample_rates.append(x[0])

#        y = list(set(total_data_points(file)))
#        data_points.append(x[0])

#print(sorted(total_channels))
   
#print (np.average(data_points))
#print (np.std(data_points))




#f = h5py.File('COOLCAT_20091227_194103_36_20091227_194103_360.hdf','r')
#chanIDs = f['DYNAMIC DATA']




'''
for dataset in sorted(chanIDs):
    print (dataset)
    dset = chanIDs[dataset]['MEASURED']
    measured = (dset[0:len(dset)])
    print ('Average: {} '.format(np.average(measured)))
    print ('Std.Dev: {} '.format(np.std(measured)))
    print ('Min: {}'.format(np.min(measured)))
    print ('Max: {}'.format(np.max(measured)))
    print ('# of Data Points: {}'.format(len(measured)))
    print ('# of Unique Data Points: {}'.format(len(set(measured))))
'''
#for dataset in sorted(chanIDs):
    
#    dataset= chanIDs[dataset]
#    dataset_attrs = dataset.attrs
#    print(dataset_attrs['SAMPLE RATE'])

#print ((all_std))

#print (len(set(all_std)))

























'''
#get metadata for chanIDs
chan_attr = chanIDs.attrs
print (list(chan_attr.keys()))

#get data and then metadata for single channel ch_86
ch_86 = chanIDs['ch_86']
print (list(ch_86.keys()))

ch_86_attr = ch_86.attrs
print (list(ch_86_attr.keys()))


#the data within ch_86
dset = ch_86['MEASURED']
print (list((dset.attrs).keys()))

#print sample rate
print (ch_86_attr['SAMPLE RATE'])

#metadata for whole file
f_attr= f.attrs
print (list(f_attr.keys()))
'''



