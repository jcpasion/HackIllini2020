import numpy as np

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