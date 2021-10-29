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
                start_frame: first useful frame of the run
                run_avg: float, average output for all pixels across all frames 
                frame_arr: uint16 np.ndarray, pixel array for all frames
                frame_avg: np.ndarray, array of the individual average pixels output  
                offset: np.ndarray, pixel array of offset (pedestal) values for the sensor
                err_dark: np.ndarray, pixel array of dark (read) noise   
        """
        self.success = success
        self.name = name
        self.filepath = None
        self.n_frames = None
        self.start_frame = None
        self.run_avg = None
        self.frame_arr = None
        self.frame_avg = None
        self.offset = None
        self.err_dark = None
    

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
    return im, n_frames - 1

def get_run(name=None, filepath_raw=None, start_frame=100):
    """
    Reads the run name and filepath from std input. Checks that the filepath is
    valid. Extracts the frame data from each file into an array, removes any metadata, and 
    returns and instance of the Run object

    returns: Run object with corresponding name, filepath, and frame_avg.
    """
    # Get name of run and create Run_path object
    if name == None:
        name = input("Input name of run, press <enter> to skip:\n")
        if name == "":
            name = None
    run = Run(True, name)
    # Get filepath and ensure it is valid
    if filepath_raw == None:
        while True:
            filepath = input("Input a valid filepath or press <enter> to exit program:\n")
            filepath_raw = r"{}".format(filepath)
        # Allow user to abort run
            if filepath == "":
                run.success = False
                exit()      
    if os.path.isfile(filepath_raw) == True:
        run.filepath = filepath_raw
    else:
        print("Error: could not find file: {}".format(filepath))
        exit()
    run.frame_arr, run.n_frames = file_t_arr(run.filepath, run.resolution)
    # Setup start frame SORT OUT INPUT LATER
    run.start_frame = start_frame
    return run


def get_multi_run(start_frame,VERBOSE=False):
    """
    Asks user to enter a valied path to a directory containing a series runs
    and askes for the indentifying string for the series of runs. Form each
    valid filename in the directory it will try to create a run object using
    get run.

    Returns: list of Run objects where the name corresponds to the filename
    for the file containing the data 
    """
    # Get valid directory from std input
    while True:
        # Get valid dir
        print("Please input a valid directory path")
        filedir = input("Press <enter> to exit program\n")
        filedir_raw = r"{}".format(filedir)
        if filedir == "":
            exit()
        if os.path.isdir(filedir_raw) == False:
            print("Error: could not find directory {}".format(filedir_raw))
            continue
        filedir_names = os.listdir(filedir_raw)
        if len(filedir_names) == 0:
            print("Error: directory is empty please enter a non-empty directory")
            continue
        break
    # Get valid name from std input
    while True:
        id = False
        print("Please input a valid identifying string for the run")
        file_id = input("Press <enter> to exit program\n")
        for filename in filedir_names:
            if file_id in filename:
                id = True
                break
        if id == True:
            break
        else: print("Error did not match identifyer to any files")

    run_sequence = []
    for filename in filedir_names:
        filetype = filename.split(".")[-1]
        if filetype == "raw":
            filepath_raw = os.path.join(filedir_raw, filename)
            run_sequence.append(get_run(name=filename, filepath_raw=filepath_raw, start_frame=start_frame))
    return run_sequence
        
                

        
                



    

            
        

        
