import numpy as np

def filter_channels_historic(in_dict,stdev_cutoff):
    #get global distribution of summary stats for each channel
    global_min = []
    global_max = []
    for key_file in in_dict:
        for key_channel in in_dict[key_file]:
            global_min.append(in_dict[key_file][key_channel]['min'])
            global_max.append(in_dict[key_file][key_channel]['max'])
    #process global_min
    global_min_mean = np.average(global_min)
    global_min_stdev = np.std(global_min)
    global_min_upper = global_min_mean + (global_min_stdev * stdev_cutoff)
    global_min_lower = global_min_mean - (global_min_stdev * stdev_cutoff)
    
    #process global_max
    global_max_mean = np.average(global_max)
    global_max_stdev = np.std(global_max)
    global_max_upper = global_max_mean + (global_max_stdev * stdev_cutoff)
    global_max_lower = global_max_mean - (global_max_stdev * stdev_cutoff)
    
    for key_file in in_dict:
        for key_channel in in_dict[key_file]:
            if in_dict[key_file][key_channel]['min'] > global_min_upper:
                del in_dict[key_file][key_channel]
            elif in_dict[key_file][key_channel]['min'] < global_min_lower:
                del in_dict[key_file][key_channel]
            if in_dict[key_file][key_channel]['max'] > global_max_upper:
                del in_dict[key_file][key_channel]
            elif in_dict[key_file][key_channel]['max'] < global_max_lower:
                del in_dict[key_file][key_channel]
    return in_dict