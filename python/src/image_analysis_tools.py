import numpy as np
import matplotlib.pyplot as plt







def graph_mean(arr):
    """
    Graphs the average of the inner dimension of a 2d np.ndarra
    
    Args:
        arr: np.ndarra 2d array to be graphed. 

    Returns:
        array of means
    """
    arr_avg = arr.mean(axis=1)
    arr_avg.reshape(-1)
    n_frames = len(arr_avg)
    arr_im_num = np.linspace(1, n_frames, n_frames)
    fig_avg = plt.figure(num="avg", figsize=[8, 6])
    ax1 = fig_avg.add_axes([0.1, 0.1, 0.8, 0.8])
    ax1.plot(arr_im_num, arr_avg)
    plt.show()
    return arr_avg
