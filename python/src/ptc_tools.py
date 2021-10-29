import numpy as np
import matplotlib.pyplot as plt

# import image_analysis_tools as iat

class PTC:
    """
    Object for organising ptc data
    """

    def __init__(self, n_runs, resolution):
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
        """
        self.s_mean = np.zeros([n_runs, *resolution], dtype=float)
        self.err_tot = self.s_mean.copy()
        self.err_fpn = self.s_mean.copy()
        self.err_gauss = self.s_mean.copy()
    
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
            self.err_fpn = np.take_along_axis(self.err_fpn, index, axis=0)
            self.err_gauss = np.take_along_axis(self.err_gauss, index, axis=0)
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


def get_ptc(run_series, offset, read_error, resolution, sort=False):
    """
    Creates calculates all required parameters a photon transfer curve in a  
    PTC object.

    Args:
        run_series: array-like, collection of Run objects corresponding to the
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
    # Create PTC object to populate with data
    n_runs = len(run_series)
    ptc = PTC(n_runs=n_runs, resolution=resolution)
    # Determine values for each run individually
    for i in range(n_runs):
        # Remove offset and determine average signal for each pixel
        run = run_series[i]
        # Useful frames
        u_frames = run.n_frames-run.start_frame
        raw = run.frame_arr.copy()
        signal = np.zeros([u_frames, *resolution], dtype="uint16")
        for j in range(run.start_frame, run.n_frames, 1):
            signal = raw[j] - offset
        ptc.s_mean[i] = signal.mean(axis=0)
        # Determine total uncertainty
        ptc.err_tot[i] = signal.std(axis=0)
        # Remove fixed pattern noise and determine gaussian noise
        err_gauss = np.zeros(run.resolution, dtype=float)
        for j in range(run.start_frame, run.n_frames, 1):
            err_gauss = err_gauss + np.square(raw[j] - raw[j-1])
        ptc.err_gauss[i] = np.sqrt(err_gauss/(2*u_frames)) 
    # Sort arrays against s_mean if sort == True
    if sort == True:
        index = ptc.s_mean.argsort(axis=0, kind="heapsort")
        ptc.index_sort(index, axis=0)
    
    # Plot output of pixel (0, 0) - remove later
    # plt.plot(ptc.s_mean[:, 0, 0], ptc.err_tot[:, 0, 0])
    # plt.show()
    return ptc


def graph_err_tot(ptc, axes, log=False, colour="g"):
    """
    Plot the total error against average signal.

    Args:
        ptc: PTC class instance; collection data for ptc curve plotting
        
        axes: matplotlib.pyplot.axes; axes on which to plot total noise

        log: bool; if set to true the log of each value is taken

        colour: str; colour of the noise plot (standard matplotlib colours)
    """
    x_vals = np.log10(ptc.s_mean[:, 1, 1])
    y_vals = np.log10(ptc.err_tot[:, 1, 1])
    axes.plot(x_vals, y_vals, color=colour, label="Total noise")


def graph_err_fpn(ptc, axes, log=False, colour="b"):
    """
    Plot the fixed pattern noise against average signal.

    Args:
        ptc: PTC class instance; collection data for ptc curve plotting
        
        axes: matplotlib.pyplot.axes; axes on which to plot the fixed pattern
            noise

        log: bool; if set to true the log of each value is taken

        colour: str; colour of the noise plot (standard matplotlib colours)
    """
    x_vals = np.log10(ptc.s_mean[:, 1, 1])
    y_vals = np.log10(ptc.err_fpn[:, 1, 1])
    axes.plot(x_vals, y_vals, color=colour, label="Fixed pattern noise")


def graph_err_gauss(ptc, axes, log=False, colour="r"):
    """
    Plot the total noise against average signal.

    Args:
        ptc: PTC class instance; collection of PTC data for curve plotting
        
        axes: matplotlib.pyplot.axes; axes on which to plot total noise

        log: bool; if set to true the log of each value is taken
        
        colour: str; colour of the noise plot (standard matplotlib colours)
    """
    x_vals = np.log10(ptc.s_mean[:, 1, 1])
    y_vals = np.log10(ptc.err_gauss[:, 1, 1]) 
    axes.plot(x_vals, y_vals, color=colour, label="Gaussian (shot) noise")


def graph_err_read(ptc, read_noise, axes, log=False, colour="r"):
    """
    Plot the total noise against average signal.

    Args:
        ptc: PTC class instance; collection of PTC data for curve plotting
        
        axes: matplotlib.pyplot.axes; axes on which to plot total noise

        log: bool; if set to true the log of each value is taken

        colour: str; colour of the noise plot (standard matplotlib colours)
    """
    # generate read noise
    
    x_vals = np.log10(ptc.s_mean[:, 1, 1])
    y_vals = np.log10(ptc.err_gauss[:, 1, 1]) 
    axes.plot(x_vals, y_vals, color=colour, label="Gaussian (shot) noise")


def graph_ptc(ptc, log=False, scale="linear"):
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
        print("Press <2> for fixed patten noise plot")
        print("Pless <3> for gaussian (shot) noise plot")
        print("Press <4> for read noise plot")
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
    # Plot relevant noise graphs depending on value of plots
    figure = plt.figure(figsize=(10, 6))
    ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])
    if "1" in plots:
        graph_err_tot(ptc, ax, log=log)
    if "2" in plots:
        graph_err_fpn(ptc, ax, log=log)
    if "3" in plots:
        graph_err_gauss(ptc, ax, log=log)
    if "4" in plots:
        graph_err_read(ptc, ax, log=log)
    ax.set_xscale(scale)
    ax.set_yscale(scale)
    ax.set(xlabel="Signal", ylabel="Noise")
    ax.legend()
    plt.show()