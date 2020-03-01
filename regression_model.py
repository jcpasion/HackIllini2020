import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as seabornInstance
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn import svm
from pandas.core.common import random_state


dset = ""
freqset = ""
regressed_streams = {}
for file in dset:
    for channel in dset[file]:
        if channel not in regressed_streams:
            regressed_streams[channel] = []
        y = dset[file][channel]
        X = ""
        
        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.2, random_state = 0)
        regressor = LinearRegression()
        regressor.fit(X_train,y_train)
        y_pred = regressor.predict(X_test)
        print("Mean Square Error: {}".format(metrics.mean_squared_error(y_test,y_pred)))
        
#X is scaled time series based on sampling time
#y is the value observed at time point x

