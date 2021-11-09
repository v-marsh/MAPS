import numpy as np
import matplotlib.pyplot as plt

# import image_analysis_tools as iat

class PTC:
    """
    Object for organising ptc data
    """

    def __init__(self, n_runs, resolution, sorting):
        """
        Class attributes:
            s_mean: np.ndarray, pixel array of each pixel's arithmetic mean
                after the offset has been removed (average signal) for each 
                run in the series 

            err_tot: np.ndarray, array of each pixel's total noise for each run
                in the series

            err_fpn: np.ndarray, array of each pixel's fixed pattern noise for
                each run in the series
                
            err_gauss: np.ndarray, array for each pixel's gaussian noise
                (shot noise) in the series
            
            sorted: bool; if set to True each pixel's values have been sorted
                against s_mean
        """
        self.s_mean = np.zeros([n_runs, *resolution], dtype=float)
        self.err_tot = self.s_mean.copy()
        self.err_fpn = self.s_mean.copy()
        self.err_gauss = self.s_mean.copy()
        self.sorted = sorting
        self.resolution = resolution
        
    
    def index_sort(self, index, axis=-1):
        """
        Sorts all arrays against index locally. NOTE: THIS MAY SORT EACH PIXEL
        DIFFERENTLY MEANING THAT IT IS NO LONGER POSSIBLE TO ANALYSE CLUSERS 
        OF PIXELS DIRECTLY. ONE MUST INSTEAD CALCULATE VALUES FROM EACH PIXEL'S
        PTC INDEPENDETLY AND THEN COMPARE THEM !!!

        Args:
            index: array-like, index to sort all arrays against. NOTE: this
                must have the same shape as the ptc arrays

            axis: int, axis along which index was sorted
        """
        if index.shape == self.s_mean.argsort(axis=axis).shape:
            self.s_mean = np.take_along_axis(self.s_mean, index, axis=0)
            self.err_tot = np.take_along_axis(self.err_tot, index, axis=0)
            # self.err_fpn = np.take_along_axis(self.err_fpn, index, axis=0)
            # self.err_gauss = np.take_along_axis(self.err_gauss, index, axis=0)
        else:
            print("Error: index shape and axes do not match ptc arrays")
            exit()
    def flatten(self):
        """
        Flattens all arrays
        """
        self.s_mean = self.s_mean.reshape(-1)
        self.err_tot = self.err_tot.reshape(-1)
        self.err_fpn = self.err_fpn.reshape(-1)
        self.err_gauss = self.err_gauss.reshape(-1)


def get_ptc(datasets, offset, read_error, resolution, sort=False):
    """
    Calculates all required parameters a photon transfer curve and stores them
    in a PTC object.

    Args:
        datasets: array-like, collection of Run objects corresponding to the
            run data used to calculate the photon transfer curve

        offset: array-like, pixel array of offset (dark values) for each
            individual pixel in the sensor.
        
        read_error: array-like, pixel array of the read noise (dark noise) for
            each individual pixel in the sensor.

        resolution: array-like, dim(2) array containing the sensor resolution

        sort: bool, if set to true then the arrays of the PTC object are 
            sorted against average signal INDIVIDUALLY FOR EACH PIXEL. This
            means that each [n, :, :] subarray may no longer contain data from
            a single run 
        
    Returns: PTC object containing the average signal, total noise, fixed
        pattern noise, and shot noise for each pixel over a single run 
        for all runs.
    """
    n_runs = len(datasets)
    ptc = PTC(n_runs=n_runs, resolution=resolution, sorting=sort)
    # Determine values for each run individually
    for i in range(n_runs):
        run = datasets[i]
        # Remove offset and determine average signal for each pixel
        raw = run.frame_arr.copy().astype(dtype=np.int64, copy=False)
        ptc.s_mean[i] = raw[run.start_frame:].mean() - offset
        ptc.err_tot[i] = raw[run.start_frame:].std()
        # # Remove fixed pattern noise and determine gaussian noise
        # err_gauss = np.zeros(run.resolution, dtype=float)
        # for j in range(run.start_frame, run.n_frames, 1):
        #     err_gauss = err_gauss + np.square(raw[j] - raw[j-1])
        # ptc.err_gauss[i] = np.sqrt(err_gauss/(2*u_frames)) 
    # Sort arrays against s_mean if sort == True
    if sort == True:
        index = ptc.s_mean.argsort(axis=0, kind="quicksort")
        ptc.index_sort(index, axis=0)
    return ptc


def graph_err_tot(ptc, axes, pixel, colour="g"):
    """
    Plot the total error against average signal.

    Args:
        ptc: PTC class instance, collection data for ptc curve plotting
        
        axes: matplotlib.pyplot.axes, axes on which to plot total noise

        pixel: array-like: cooridinates of pixel to plot

        colour: str, colour of the noise plot (standard matplotlib colours)
    """
    axes.plot(ptc.s_mean[:, pixel[0], pixel[1]], ptc.err_tot[:, pixel[0], pixel[1]], color=colour, label="Total noise")


# def graph_err_fpn(ptc, axes, colour="b"):
#     """
#     Plot the fixed pattern noise against average signal.

#     Args:
#         ptc: PTC class instance, collection data for ptc curve plotting
        
#         axes: matplotlib.pyplot.axes, axes on which to plot the fixed pattern
#             noise

#         colour: str, colour of the noise plot (standard matplotlib colours)
#     """
#     axes.plot(ptc.s_mean[:, 0, 0], ptc.err_fpn[:, 0, 0], color=colour, \
#         label="Fixed pattern noise")


# def graph_err_gauss(ptc, axes, colour="r"):
#     """
#     Plot the total noise against average signal.

#     Args:
#         ptc: PTC class instance, collection of PTC data for curve plotting
        
#         axes: matplotlib.pyplot.axes, axes on which to plot total noise

#         colour: str, colour of the noise plot (standard matplotlib colours)
#     """
#     axes.plot(ptc.s_mean[:, 0, 0], ptc.err_gauss[:, 0, 0], color=colour, \
#         label="Gaussian (shot) noise")


# def graph_err_read(read_noise, axes, colour="r"):
#     """
#     Plot the total noise against average signal.

#     Args:
#         ptc: PTC class instance, collection of PTC data for curve plotting
        
#         axes: matplotlib.pyplot.axes, axes on which to plot total noise

#         colour: str, colour of the noise plot (standard matplotlib colours)
#     """
#     # generate read noise
#     axes.plot(ptc.s_mean[:, 0, 0], ptc.err_gauss[:, 0, 0], color=colour, \
#         label="Gaussian (shot) noise")


def graph_ptc(ptc):
    """
    Graphs ptc curves depending on user input.

    Args:
        ptc: PTC class instance, collection of PTC data for curve plotting
    """
    # Take user input to determine the required noise plots
    while True:
        fail = False
        print("Choose PTC plot(s) from the list below:")
        print("Press <1> for total noise plot")
        # print("Press <2> for fixed patten noise plot")
        # print("Pless <3> for gaussian (shot) noise plot")
        # print("Press <4> for read noise plot")
        print("Press <enter> to exit program")
        plots = input()
        if plots == "":
            exit()
        for char in plots:
            if char not in ("1", "2", "3", "4"):
                print("Error: \"{}\" is not a valid plot choice".format(char))
                print("Please only enter valid plot choices")
                fail = True
                break
        if fail == False:
            break
    # User input to determine pixel to plot
    while True:
        print("Please enter pixel x value in from {}".format(ptc.resolution[0]))
        x_val = input()
        try:
            x_val = int(x_val)
        except:
            print("Please input and integer")
            continue
        if x_val > ptc.resolution[0] or x_val < 0:
            print("Error: Invalid x value \"{}\", must be in (0, {})"\
                .format(x_val, ptc.resolution[0]))
            continue
        else:
            break
    while True:
        print("Please enter pixel y value in from {}".format(ptc.resolution[1]))
        y_val = input()
        try:
            y_val = int(y_val)
        except:
            print("Please input and integer")
            continue
        if y_val > ptc.resolution[1] or y_val < 0:
            print("Error: Invalid x value \"{}\", must be in (0, {})"\
                .format(y_val, ptc.resolution[1]))
            continue
        else:
            break
    pixel = (x_val, y_val)
    # Plot relevant noise graphs depending on value of plots
    figure = plt.figure(figsize=(10, 6))
    ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])
    if "1" in plots:
        graph_err_tot(ptc, ax, pixel)
    # if "2" in plots:
    #     graph_err_fpn(ptc, ax)
    # if "3" in plots:
    #     graph_err_gauss(ptc, ax)
    # if "4" in plots:
    #     graph_err_read(ptc, ax)
    # ax.set_xscale("log")
    # ax.set_yscale("log")
    ax.set(xlabel="Signal", ylabel="Noise")
    ax.legend()
    plt.show()