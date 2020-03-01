#!/usr/bin/env python
  
import os
import h5py
import numpy as np
import pandas as pd
import statistics
from newer_hdf import *

directory = os.listdir()
#create a dataframe with good exploratory data columns
lst = []
cols= ['filename','channel']
for file in directory:
    if file.endswith('.hdf'):
        f= h5py.File(file,'r')
        chanIDs = f['DYNAMIC DATA']

        for dataset in chanIDs:
            dset = chanIDs[dataset]['MEASURED']
            measured = (dset[0:len(dset)])

            att = chanIDs[dataset].attrs
            sample = att['SAMPLE RATE']

            lst.append([file, dataset,sample,len(measured), np.average(measured), np.std(measured), np.min(measured), np.max(measured)])

df=pd.DataFrame(lst,columns=['filename','channel','sample_rate','number_data_points','average','stdev','min','max'])

print(df)
