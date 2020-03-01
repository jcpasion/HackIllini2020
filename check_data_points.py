#!/usr/bin/env python

import os
import h5py
import numpy as np
import statistics

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

    return (number_data_points[0])

directory = os.listdir()

#initalize data points list for later statistics
#initialize outlier files list
data_points=[]
bad_files= []

for file in directory:
    if file.endswith('.hdf'):
        #get number of data points in a file
        print(total_data_points(file))
        data_points.append(total_data_points(file))

mean = (np.mean(data_points))
std  = np.std(data_points)


print ('mean: {}'.format(mean))
print ('std: {}'.format(std))

upper_bound = mean + (2*std)
lower_bound = mean - (2*std)

print ('lower_bound: {}'.format(lower_bound))
print ('upper_bound: {}'.format(upper_bound))


#append outlier files to a list so future analysis can exclude them
for file in directory:
    if file.endswith('.hdf'):
        if total_data_points(file) < lower_bound or total_data_points(file) > upper_bound:
            bad_files.append(file)

print (bad_files)
