import numpy as np
import matplotlib.pyplot as plt


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

    # Determine start point for calculating the mean

    return arr_avg

def graph_pixel(arr, coords):
    """
    
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
