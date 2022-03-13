import os
import sys

sys.path.append(r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python_old\src")
import pickle
import matplotlib.pyplot as plt
import ptc_tools

def graph_err_tot(ptc, axes, pixel, colour="g"):
    """
    Plot the total error against average signal.

    Args:
        ptc: PTC class instance, collection data for ptc curve plotting
        
        axes: matplotlib.pyplot.axes, axes on which to plot total noise

        pixel: array-like: cooridinates of pixel to plot

        colour: str, colour of the noise plot (standard matplotlib colours)
    """
    axes.scatter(ptc.s_mean[:, pixel[0], pixel[1]], ptc.err_tot[:, pixel[0], pixel[1]], color=colour, label="Total noise")


def graph_err_smooth(ptc, axes, pixel, smooth=1, colour="r"):
    smootherr = ptc.err_tot[:, pixel[0], pixel[1]]
    n_frames = smootherr.shape[0]
    for i in range(n_frames):
            frame_avg = 0
            for j in range(2*smooth + 1):
                k = i + j - smooth
                if k < 0:
                    k = 0
                elif k > n_frames - 1:
                    k = n_frames - 1
                frame_avg += smootherr[k]
            frame_avg /= 2*smooth + 1
            smootherr[i] = frame_avg
    axes.plot(ptc.s_mean[:, pixel[0], pixel[1]], smootherr, color=colour, label="Total noise (smoothed)")


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
    while True:
        print("Please enter smoothing")
        smoothing = input()
        try:
            smoothing = int(y_val)
        except:
            print("Please input and integer")
            continue
        if y_val < 1:
            print("Error: Invalid smoothing, must be greater than or equal to 1")
            continue
        else:
            break
    # Plot relevant noise graphs depending on value of plots
    figure = plt.figure(figsize=(10, 6))
    ax = figure.add_axes([0.1, 0.1, 0.8, 0.8])
    if "1" in plots:
        graph_err_tot(ptc, ax, pixel)
        graph_err_smooth(ptc, ax, pixel, smooth=smoothing)
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


if __name__ == "__main__":
    print("Please enter path to PTC curve")
    ptc_path = input()
    if os.path.isfile(ptc_path) == True:
        print("Recived path to run ptc object\n")
        with open(ptc_path, "rb") as file:
            ptc = pickle.load(file)
        print("PTC \"{}\" successfully loaded")
    else:
        print("Invalid path")
        exit()
    while True:
        next = input("graph again")
        if next == "y":
            graph_ptc(ptc)
        else:
            break