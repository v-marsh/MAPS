import os
import sys
sys.path.append(r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python_old\src")
import pickle
import ptc_tools
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

filepath = r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python_old\lib\PT_curves\w4_ptc2_sorted.npy"
gainpath = r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python_old\lib\Gain"
fullpath = r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python_old\lib\Full_well"
noisepath= r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python_old\lib\Read_noise"

def fit_func(x, a, b):
    return a*x + b


def fit_curve(ptc, cutoff):
    shape = ptc.s_mean.shape
    parameters = np.zeros([2, *shape[1:]], dtype=float)
    for i in range(520):
        print(i)
        for j in range(520):
            if cutoff[i, j] >= 2:
                parameters[:, i, j] = curve_fit(fit_func, 
                                                  ptc.s_mean[:cutoff[i, j], i, j],
                                                  ptc.err_tot[:cutoff[i, j], i, j])[0]
    gain = 1/parameters[0]
    read_noise = parameters[1]
    return (gain, read_noise)


def get_peak(ptc, smooth=3):
    print("Smoothing over {} frames".format(smooth))
    shape = ptc.err_tot.shape
    array = ptc.err_tot.reshape(shape[0], -1)
    n_points = array.shape[1]
    for i in range(n_points):
        frame_avg = np.zeros(shape[0], dtype=float)
        for j in range(2*smooth + 1):
            k = i + j - smooth
            if k < 0:
                k = 0
            elif k > n_points - 1:
                k = n_points - 1
            frame_avg += array[:, k]
        frame_avg /= 2*smooth + 1
        array[:, i] = frame_avg
    array = array.reshape(shape)
    return array.argmax(axis=0)


def save_arr(array, arr_name, savepath):
    while True:
        print(f"Please choose a filename to save {arr_name}")
        filename = input()
        filepath = os.path.join(savepath, filename)
        if filename == "":
            return
        if os.path.isfile(filepath):
            print("Error filename already in use!")
            continue
        break
    with open(filepath, "wb") as file:
        np.save(file, array)


if __name__ == "__main__":
    # get ptc put into ptc variable
    with open(filepath, "rb") as file:
        ptc = pickle.load(file)
    peak = get_peak(ptc)
    gain, read_noise = fit_curve(ptc, peak)
    # bad_coords = np.where(abs(gain) > 200)
    # gain[bad_coords] = 0
    # bad_coords = np.where(gain < 0)
    # gain[bad_coords] = 0
    plt.imshow(gain)
    plt.show()
    # Save gain
    save_arr(gain, "gain", gainpath)
    # calc full well and save
    full_well = peak*gain
    save_arr(full_well, "full well capacity", fullpath)
    save_arr(read_noise, "read noise", noisepath)
    
    

    



    