import os
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 16})
import numpy as np


def keep_bins(array, index):
    return map(lambda arr: arr[index], array)


filepath = r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python_old\lib\Dynamic_range\dynamic_range_3smooth_w2_ptc"
savepath = r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\Final_graphs"
data_type = "Dynamic Range"
units = "dB"
title = f"{data_type} for Vanilla Sensor"
xlabel = f"{data_type} [{units}]"
ylabel = f"Number of Pixels"
hist_discrete = False
discrete_step = 1
n_bins_cont = 2000
cutoff = 5

if __name__ == "__main__":
    # load array
    try:
        array = np.load(filepath)
    except SyntaxError:
        print("Filepath is invalid")
    # Get past Nan and inf negative values
    bad_coords = np.where(np.isnan(array))
    array[bad_coords] = 0
    bad_coords = np.where(np.isinf(array))
    array[bad_coords] = 0
    bad_coords = np.where(array < 0)
    array[bad_coords] = 0
    # calculate mean and noise(std.dev.)
    mean = array.mean()
    noise = array.std()
    # Create histogram of values
    if hist_discrete == True:
        # Create bin array with bins integer bins between max an min
        bin_edge = np.arange(array.min() - 0.5, \
            array.max() + 0.5, step=discrete_step, dtype=float)
        # Determine bin probabilities
        bin_prob = np.histogram(array.reshape[-1], bins=bin_edge)[0]
        # Determine bin mids
        bin_mid = (bin_edge[:-1] + 0.5).astype(int)
        # Remove empty bins
        non_empty = bin_prob.nonzero()
        bin_prob, bin_mid = keep_bins((bin_prob, bin_mid), non_empty)
        # Remove bins more than 5 std away
        good_bins = np.where(np.abs(bin_mid) < mean+cutoff*noise)
        bin_prob, bin_mid = keep_bins((bin_prob, bin_mid), good_bins)
    else:
        bin_prob, bin_edge = np.histogram(array, bins=n_bins_cont)
        # Create central bin values
        bin_mid = bin_edge[:-1] + (bin_edge[1]-bin_edge[0])/2
        # Remove bins that are more than 5 std away
        good_bins = np.where(np.abs(bin_mid) < mean+cutoff*noise)
        bin_prob, bin_mid = keep_bins((bin_prob, bin_mid), good_bins)
        good_bins = np.where(np.abs(bin_mid) > mean-cutoff*noise)
        bin_prob, bin_mid = keep_bins((bin_prob, bin_mid), good_bins)
        # Remove empty bins
        non_empty = bin_prob.nonzero()
        bin_prob, bin_mid = keep_bins((bin_prob, bin_mid), non_empty)
        # Remove 0 bin
        bin_prob, bin_mid = map(lambda arr: arr[1:], (bin_prob, bin_mid))
    
    
    # Remove bad values in imshow
    bad_pix = np.where(np.abs(array) > mean+cutoff*noise)
    array[bad_pix] = 0 

    # Create figure
    figure = plt.figure(figsize=[12, 6])
    figure.suptitle(title)
    im_ax = figure.add_axes([0.075, 0.05, 0.45, 0.9])
    im_ax.set(title="Sensor Array", xlabel="Column Number", ylabel="Row Number")
    pos = im_ax.imshow(array)
    figure.colorbar(pos, ax=im_ax, shrink=0.8)
    hist_ax = figure.add_axes([0.6, 0.14, 0.36, 0.72])
    hist_ax.plot(bin_mid, bin_prob)
    hist_ax.set(xlabel=xlabel, ylabel=ylabel, title="Frequency Distribution")
    plt.show(block=False)
    while True:
        print("Save (y/n)?")
        save = input()
        if save == "y":
            break
        if save == "n":
            exit()
        else:
            continue
    while True:
        print("Please input a filename to save")
        filename = input()
        filename = f"{filename}.png"
        filepath = os.path.join(savepath, filename)
        if os.path.isfile(filepath):
            print("Error: filename already in use")
            continue
        break
    figure.savefig(filepath)
    print(filename)
    print(f"mean={mean}")
    print(f"noise={noise}")
