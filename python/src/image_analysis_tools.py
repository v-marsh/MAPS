import numpy as np
import matplotlib.pyplot as plt

def file_t_arr(filepath, resolution = [520, 520], VERBOSE=False):
    """
    Extracts data from file into an numpy.ndarray. Removes metadata pixels
    
    Args:
        filepath: str, path to the imput file containing the sensor data
        resolution: resolution of the sensor
        VERBOSE: bool, if set to True then the number of frames and the 
            output array will be printed to std output

    Returns:
    A [n_frame, n_pixels] numpy.ndarray 
    """
    im = np.fromfile(filepath, dtype="uint16")
    pix_per_frame = 520*520 + 2
    # Reshapes into 2d array so the pixels are sorted into frames
    n_frames = int(im.size / pix_per_frame)
    im = im.reshape([n_frames, pix_per_frame])
    # Removes metdata in frame 0 and pixels 0, 1 in each subsequent frame
    im = im[1:, 2:]
    im.reshape([n_frames - 1, *resolution])
    if VERBOSE == True:
        print("number of frames = {}".format(n_frames))
        print(im)
    return im


def graph_mean(arr):
    """
    Graphs the average of the inner dimension of a 2d np.ndarra
    
    Args:
        arr: np.ndarra 2d array to be graphed. 

    Returns:
        void
    """
    arr_avg = arr.mean(axis=1)
    arr_avg.reshape(-1)
    n_frames = len(arr_avg)
    arr_im_num = np.linspace(1, n_frames, n_frames)
    fig_avg = plt.figure(num="avg", figsize=[8, 6])
    fig_avg.add_axes(ax1)
    ax1.plot(arr_im_num, arr_avg)
    plt.show("avg")
