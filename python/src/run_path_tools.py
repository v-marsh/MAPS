import sys
import os

import numpy as np


class Prog_data():
    saved_runs = {}
    free_index = 0

    def print_saved(self):
        """
        Prints the name of each saved run and the number of datasets contained
        within to std. output
        """
        print("Loaded runs are:")
        
        if len(self.saved_runs) == 0:
            print("None")
        else:
            for key in self.saved_runs:
                print("Run name: {}".format(key))
                print("Number of datasets in run: {}".format(len(\
                self.saved_runs[key])))
        print("\n")

    def del_run(self, run_name):
        """
        Deletes the run corresponding to run_name in self.saved_runs if it
        exists
        
        Args:
            run_name: str; name of run to delete   
        """
        if run_name in self.saved_runs.keys():
            self.saved_runs.pop(run_name)
        else:
            print("Error: did not find run \"{}\", aborting".format(run_name))


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
        self.use_pix = None

    def __len__(self):
            return 1
    
def get_run_name(prog_data):
    """
    Asks user to input a run name in std. input
    
    Args:
        prog_data: Prog_data class instance; all imported runs so far

    Returns: str; the run name inputted by the user
    """
    while True:
        print("Please input a unique run name")
        print("Press <enter> to automatically assign run name")
        run_name = input()
        if run_name == "":
            run_name = prog_data.free_index
            prog_data.free_index += 1
            return run_name
        elif run_name in prog_data.saved_runs:
            print("Error run name is already in use")
            continue
        else:
            return run_name
        


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

def get_single_run(name, filepath, start_frame):
    """
    Extracts the frame data from filepath file into an array, removes any 
    metadata and returns and instance of the Run object

    Args:
        name: str; name of the dataset
    returns: Run object with corresponding name, filepath, and frame_avg.
    """
    run = Run(True, name)
    run.filepath = filepath
    run.frame_arr, run.n_frames = file_t_arr(run.filepath, run.resolution)
    run.start_frame = start_frame
    return run


def get_multi_run(dirpath, start_frame, VERBOSE=False):
    """
    Asks user to enter a valied path to a directory containing a series runs
    and askes for the indentifying string for the series of runs. Form each
    valid filename in the directory it will try to create a run object using
    get_single_run.

    Returns: list of Run objects where the name corresponds to the filename
    for the file containing the data 
    """
    # # Get valid directory from std input
    # while True:
    #     # Get valid dir
    #     print("Please input a valid directory path")
    #     filedir = input("Press <enter> to exit program\n")
    #     filedir_raw = r"{}".format(filedir)
    #     if filedir == "":
    #         exit()
    #     if os.path.isdir(filedir_raw) == False:
    #         print("Error: could not find directory {}".format(filedir_raw))
    #         continue
    #     filedir_names = os.listdir(filedir_raw)
    #     if len(filedir_names) == 0:
    #         print("Error: directory is empty please enter a non-empty directory")
    #         continue
    #     break
    # Get valid name from std input
    dir_filenames = os.listdir(dirpath)
    if len(dir_filenames) == 0:
        print("Error: directory \"{}\" is empty, aborting!"\
            .format(dirpath))
        return
    while True:
        print("Please input an identifier for filenames belonging to the run")
        run_id = input()
        for filename in dir_filenames:
            if run_id in filename:
                run_id = True
                break
        if run_id == True:
            break
        else:
            print("Error: identifier \"{}\"did not match to any filenames, aborting"\
                .format(run_id))
    multi_run = []
    for filename in dir_filenames:
        filetype = filename.split(".")[-1]
        if filetype == "raw":
            filepath = os.path.join(dirpath, filename)
            multi_run.append(get_single_run(name=filename,\
                filepath=filepath, start_frame=start_frame))
    return multi_run