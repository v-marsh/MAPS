import sys
import os

import numpy as np


class Run():
    resolution = (520, 520) 

    def __init__(self, success, name):
        """
        Args:
            success: bool, indicates whether self.filepath is a valid path
            name: str, name of the run

        returns:
            Instance of the Run object with additional arguments:
                filepath: str, path to run data
                n_frames: int, the number of frames in the specific run
                run_avg: float, average output for all pixels across all frames 
                frame_arr: np.ndarray, pixel array for all frames
                frame_avg: np.ndarray, array of the mean output for all pixels    
        """
        self.success = success
        self.name = name
        self.filepath = None
        self.n_frames = None
        self.run_avg = None
        self.frame_arr = None
        self.frame_avg = None
    

def file_t_arr(filepath, resolution, VERBOSE=False):
    """
    Extracts data from file into an numpy.ndarray. Removes metadata pixels
    
    Args:
        filepath: str, path to the imput file containing the sensor data
        resolution: array-like, resolution of the sensor
        VERBOSE: bool, if set to True then the number of frames and the 
            output array will be printed to std output

    Returns:
    A [n_frame, n_pixels] numpy.ndarray 
    """
    # check for valid resolution
    if len(resolution) != 2:
        print("Error: invalid resolution, check resolution in Run class.")
        return None
    im = np.fromfile(filepath, dtype="uint16")
    pix_per_frame = resolution[0]*resolution[1] + 2
    # Reshapes into 2d array so the pixels are sorted into frames
    n_frames = int(im.size / pix_per_frame)
    im = im.reshape([n_frames, pix_per_frame])
    # Removes metdata in frame 0 and pixels 0, 1 in each subsequent frame
    im = im[1:, 2:]
    im = im.reshape([n_frames - 1, 520, 520])
    if VERBOSE == True:
        print("number of frames = {}".format(n_frames))
        print(im)
    return im


def get_run():
    """
    Reads the run name and filepath from std input. Checks that the filepath is
    valid. Extracts the frame data from each file into an array, removes any metadata, and 
    returns and instance of the Run object

    returns: Run object with corresponding name, filepath, and frame_avg.
    """
    # Get name of run and create Run_path object
    name = input("Input name of run, press <enter> to skip:\n")
    
    if name == "":
        name = None
    run = Run(True, name)
    # Get filepath and ensure it is valid
    while True:
        filepath = input("Input a valid filepath or press <enter> to exit program:\n")
        filepath_raw = r"{}".format(filepath)
    # Allow user to abort run
        if filepath == "":
            run.success = False
            exit()      
        if os.path.isfile(filepath_raw) == True:
            run.filepath = filepath_raw
            break
        print("Error: could not find file: {}".format(filepath))
    run.frame_arr = file_t_arr(run.filepath, run.resolution)

    return run
            
        

        
