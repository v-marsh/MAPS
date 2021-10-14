import sys
import os

class Run_setup():

    def __init__(self, success, name, filepath=None):
        """
        Args:
            success: bool, indicated if self.filepath is a valid path
            name: str, name of the run
            filepath: raw str, path to the run data 
        """
        self.success = success
        self.name = name
        self.filepath = filepath


class Run():
    
    def __init__(self, Name, n_frames):
        self.name = Name
        self.frame_tot = n_frames
        self.frame_arr = None
        self.frame_avg = None
        self.avg_out = None
    

def file_t_arr(filepath, resolution = [520, 520], VERBOSE=False):
    """
    Extracts data from file into an numpy.ndarray. Removes metadata pixels
    
    Args:
        filepath: str, path to the imput file containing the sensor data
        resolution: resolution of the sensor
        VERBOSE: bool, if set to True then the number of frames and the 
            output array will be printed to std output

    Returns:
    A [n_frame, n_pixels] numpy.ndarray 
    """
    im = np.fromfile(filepath, dtype="uint16")
    pix_per_frame = 520*520 + 2
    # Reshapes into 2d array so the pixels are sorted into frames
    n_frames = int(im.size / pix_per_frame)
    im = im.reshape([n_frames, pix_per_frame])
    # Removes metdata in frame 0 and pixels 0, 1 in each subsequent frame
    im = im[1:, 2:]
    im.reshape([n_frames - 1, *resolution])
    if VERBOSE == True:
        print("number of frames = {}".format(n_frames))
        print(im)
    return im


def get_run():
    """
    Reads the name and path of a run from std input and checks whether the path exists

    returns: Run_setup object
    """
    name = input("Input name of run, press <enter> to skip:")
    # Get name of run and create Run_path object
    if name == "\n":
        name = None
    run_setup = Run_setup(True, name)
    # Get filepath and ensure it is valid
    while True:
        filepath = input("Input a valid filepath:")
        filepath_raw = r"{}".format(filepath)       
        if os.path.isfile(filepath_raw) == True:
            run_setup.filepath = filepath_raw
            break
        print("Error: could not find file: {}".format(filepath))
        filepath = input("Please enter a valid filepath or press <enter> to exit program")
        # Allow user to abort run
        if filepath == "\n":
            run_setup.success = False
    return run_setup
            
        

        
