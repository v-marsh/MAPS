import os

import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats


def graph_mean(arr, smooth=None, resolution=(520, 520)):
    """
    Graphs the average of the inner dimension of a 2d np.ndarra
    
    Args:
        arr: np.ndarra 2d array to be graphed. 

    Returns:
        array of means
    """
    pixels = resolution[0]*resolution[1]
    arr = arr.reshape([-1, pixels])
    arr_avg = arr.mean(axis=1)
    arr_avg.reshape(-1)
    n_frames = len(arr_avg)

    # Sort out smoothing
    if smooth != None and type(smooth) == int:
        print("Smoothing over {} frames".format(smooth))
        for i in range(n_frames):
            frame_avg = 0
            for j in range(2*smooth + 1):
                k = i + j - smooth
                if k < 0:
                    k = 0
                elif k > n_frames - 1:
                    k = n_frames - 1
                frame_avg += arr_avg[k]
            frame_avg /= 2*smooth + 1
            arr_avg[i] = frame_avg

    arr_im_num = np.linspace(1, n_frames, n_frames)
    fig_avg = plt.figure(num="avg", figsize=[8, 6])
    ax1 = fig_avg.add_axes([0.1, 0.1, 0.8, 0.8])
    ax1.plot(arr_im_num, arr_avg)
    plt.show()
    return arr_avg


def graph_pixel(arr, coords):
    """
    Graphs the output of a single pixel in the array given by coords

    Args:
        arr: array-like, array of all pixels across all frames
        coords: array-like dim[2], the coordinates of the pixel

    returns:
    """
    y_coord = coords[0]
    x_coord = coords[1]
    fig_pixel = plt.figure(num="pixel", figsize=[8, 6])
    ax1 = fig_pixel.add_axes([0.1, 0.1, 0.8, 0.8])
    x_vals = np.arange(1, len(arr) + 1, 1)
    print("Len arr = {}".format(len(arr)))
    y_vals = arr[:, y_coord, x_coord].reshape(-1)
    ax1.plot(x_vals, y_vals)
    plt.show()

def show_frame(frame_arr):
    plt.imshow(frame_arr)
    plt.show()


def get_noise(arr):
    """
    Calculates the noise of one std deviation for each pixel in the sensor
    
    Args:
        arr: np.ndarray, array of pixels over all frames

    returns: An array of noise values with the dimensions of the sensor
    """
    noise_arr = arr.std(axis=0)
    # Choose whether to save
    print("Please enter a filename to save noise")
    name =  input("Press <enter> to skip\n")
    if name != "":
        dirpath = r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python\lib\Dark_Noise"
        filepath = os.path.join(dirpath, name)
        with open(filepath, "wb") as f:
            np.save(f, noise_arr)
        return noise_arr


            
        
    return noise_arr

def get_offset(arr):
    """
    Calculates the pedestal for each pixel in the sensor

    Args:
        arr: np.ndarray, array of pixels over all frames

    returns: An array of pedestal values with the dimensions of the sensor
    """
    ped_arr = arr.mean(axis=0)
    print("Please enter a filename to save offset")
    name =  input("Press <enter> to skip\n")
    if name != "":
        dirpath = r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python\lib\Dark_Offset"
        filepath = os.path.join(dirpath, name)
        with open(filepath, "wb") as f:
            np.save(f, ped_arr)
    return ped_arr


def chi_sqr_test(xvals, yvals, mean, std):
    """
    Chi Square test against gaussian distribution

    Args:
        x_vals: array-like; x values of graph to test

        y_vals: array-like; y values of graph to test

        mean: float; arithmetic mean of the graph to test

        std: float; standard deviation of the graph to test
    """
    try:
        len(xvals) == len(yvals)
    except:
        raise ValueError("The shape of xvals does not equal the shape of yvals")
    
    N = len(xvals)
    chi2 = 0
    zvals = (xvals - mean)/ std
    theoretical = lambda x : stats.norm.cdf(x)
    for i in range(len(xvals)):
        chi2 += (yvals[i]/N - theoretical(zvals[i]))**2 / theoretical(zvals[i])
    return  chi2 * N


def check_gauss(run, hpb=20):
    """
    Args:
        run: Run class instance;
        hpb: float; average hits per bin
    """
    # determine the number of frames for optimal bin values
    u_frames = run.n_frames - run.start_frame
    bin_dat = np.zeros([2, n_bins], dtype=float)
    
    # Check each individual pixel
    for i in range(run.resolution[0]):
        for j in range(run.resolution[1]):
            n_bins = range(np.min(run.frame_arr[:, i, j]) - 0.5, \
                np.max(run.frame_arr[:, i, j]) + 0.5, 1)
            bin_dat[1], bin_edge = np.histogram(run.frame_arr[:, i, j], \
                bins=n_bins, density=True)
            for k in range(n_bins):
                bin_dat[0, k] = (bin_edge[k+1]+bin_edge[k])/2
            del bin_edge
            # sorting
            plt.plot(bin_dat[0], bin_dat[1])
            # plt.hist(run.frame_arr[:, i, j], bins=n_bins, density=True)
            plt.show()
            
    # # Check all pixels
    # normal_frame_arr = np.zeros(run.frame_arr.shape, dtype=float)
    # for i in range(run.start_frame, run.n_frames, 1):
    #     normal_frame_arr[i] = (run.frame_arr[i] - run.offset) / run.err_dark
    # n_bins = int(u_frames * run.resolution[0] / hpb)
    # normal_frame_arr = normal_frame_arr.reshape(-1)
    # plt.hist(normal_frame_arr, bins=n_bins, density=True)
    plt.show()