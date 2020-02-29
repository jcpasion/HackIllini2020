def get_bin_sizes(dset,num_bins,percent_threshold):
    bin_dist = np.histogram(dset,num_bins)
    bin_sizes = bin_dist[0]
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
            good_dset.append(None)
        else:
            good_dset.append(entry)
    return good_dset