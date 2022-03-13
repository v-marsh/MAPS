import sys
import os

import numpy as np

ETS = "Press <enter> to skip"


class Prog_data():
    saved_ptc = {}
    saved_runs = {}
    free_run_name = 0
    free_ptc_name = 0

    def print_saved_all(self):
        self.print_saved_runs()
        self.print_saved_ptc()

    def print_saved_runs(self):
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

    def print_saved_ptc(self):
        """
        Prints the name of each saved PT curve
        """
        print("Loaded PT curves are:")
        
        if len(self.saved_ptc) == 0:
            print("None")
        else:
            for key in self.saved_ptc:
                print("PT curve name: {}".format(key))
                print("PT curve sorting: {}".format(\
                    self.saved_ptc[key].sorted))
        print("\n")

    def new_run_name(self):
        """
        Asks user to input a unique run name in std. input or have it
        automatically assigned
        
        Returns: str; the run name entered by the user
        """
        while True:
            print("Please input a unique run name")
            print("Press <enter> to automatically assign name")
            run_name = input()
            if run_name == "":
                run_name = str(self.free_run_name)
                self.free_run_name += 1
                return run_name
            elif run_name in self.saved_runs:
                print("Error run name is already in use")
                continue
            else:
                return run_name

    def new_ptc_name(self):
        """
        Asks user to input a unique PT curve name in std. input or have it
        automatically assigned

        Returns: str; the Pt curve name entered by the user
        """
        while True:
            print("Please input a unique PT curve name")
            print("Press <enter> to automatically assign name")
            ptc_name = input()
            if ptc_name == "":
                ptc_name = str(self.free_ptc_name)
                self.free_ptc_name += 1
                return ptc_name
            elif ptc_name in self.saved_ptc:
                print("Error run name is already in use")
                continue
            else:
                return ptc_name

    def get_run_name(self):
        """
        Asks user to input a run name in std. input and checks if it exists in
        saved_runs, i.e. if it is a valid key

        Returns: run name; if it is a valid key in saved_runs
            None; if the run name is not a valid key in saved_runs 
        """
        self.print_saved_runs()
        print("Please choose a run to analyse")
        run_name = input()
        if run_name in self.saved_runs:
            print("Run \"{}\" exists".format(run_name))
        else:
            print("Could not find run \"{}\", aborting!".format(run_name))
            return None
        # Add extra checks here as neccessary
        return run_name
    
    def get_ptc_name(self):
        """
        Asks user to input a PT curve name in std. input and checks if it
        exists in saved_ptc, i.e. if it is a valid key
        
        Returns: PT curve name; if it is a valid key in save_ptc
            None; if the PT curve name is not a valid key in saved_ptc
        """
        self.print_saved_ptc()
        print("Please choose a run to analyse for PT curve")
        ptc_name  = input()
        if ptc_name in self.saved_ptc:
            print("PT curve \"{}\" exists".format(ptc_name))
        else:
            print("Could not find run \"{}\", aborting!".format(ptc_name))
            return None
        # Add extra checks here as neccessary
        return ptc_name

    def check_ptc_req(self, run_name):
        """
        Checks if a valid run fulfills the requirements for PT curve analysis

        Returns: True; if the run satisfies the requirements
            False; if the run does not satisfy teh requirments 
        """
        run_len = len(self.saved_runs[run_name])
        if run_len > 1:
            print("Run \"{}\" contains {} datasets".format(run_name, run_len))
        else:
            error = "Run \"{}\" contains \"{}\", ".format(run_name, run_len)
            error += "PT curves require at least 2 datasets, aborting!" 
            print(error)
            return False
        # Add more requirements here if neccessary
        return True
    
    def get_run_num(self, run):
        """
        Asks user to select run number from multi run
        
        Args:
            run: array-like; collection of Run class instances
            
        Returns: Run number given that it exists, else: None
        """
        max_run_num = len(self.saved_runs[run])
        if max_run_num == 1:
            return 1
        while True:
            print("Please choose run number in range (1, {}) for analysis"\
                .format(max_run_num))
            print(ETS)
            run_num = input()
            if run_num == "":
                return None
            try:
                run_num = int(run_num)
            except:
                print("Error: please enter an integer")
                continue
            if run_num > max_run_num or run_num < 0:
                print("Error: please enter a number between 1 and {}"\
                    .format(max_run_num))
                continue            
            else:
                break
        return run_num

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

    def del_ptc(self, ptc_name):
        """
        Deletes the PT curve corresponding to ptc_name in self.saved_ptc if it
        exists
        
        Args:
            ptc_name: str; name of PT curve to delete   
        """
        if ptc_name in self.saved_runs.keys():
            self.saved_ptc.pop(ptc_name)
        else:
            print("Error: did not find PT curve \"{}\", aborting"\
                .format(ptc_name)) 

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


def get_multi_run(dirpath, start_frame):
    """
    Asks user for an indentifier and tried to match it to a filename in the
    directory at the end of dirpath. If a valid filename is found 
    it will try to create a list of multiple run objects using get_single_run.

    Args:
        dirpath: raw str; valid path to directory

        start_frame: int; first useful frame in each run object

    Returns: list of Run objects where the name corresponds to the filename
    for the file containing the data 
    """
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