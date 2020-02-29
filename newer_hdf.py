#!/usr/bin/env python

import os
import h5py
import numpy as np
import statistics

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



    
def get_channel_average(dset):
    #get average measurement of a channel
    #input: channel column dataset
    #output: average of the column

    channel = chanIDs[dset]['MEASURED']
    measured = dset[0:len(dset)]
    
    return (np.average(measured))


x = total_channel('COOLCAT_20110830_114419_85_20110830_114419_852.hdf')   
print (x)

sample_rates = []
data_points = []
total_channels = []
for file in directory:
    if file.endswith('.hdf'):
        f = h5py.File(file,'r')
        chanIDs = f['DYNAMIC DATA']
         
        for channel in chanIDs:
            print(get_channel_average(channel))

    
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



