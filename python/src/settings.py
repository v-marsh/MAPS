import os
import numpy as np
from time import sleep

noise = "Dark_test1.npy"
offset = "Dark_test1.npy"

class Settings():
    """
    Settings class for image analysis in the MAPS experiment

    Args:
        start_frame: int, the first frame of the run that is used for analysis
        end_frame: int, the final frame in the run that is used for analysis
    """
    def __init__(self, src_path, default_offset=offset, default_noise=noise):
        self.src_path = src_path
        self.offset_filepath = self.get_offset_path(default_offset)
        self.noise_filepath = self.get_noise_path(default_noise)
        self.resolution = (520, 520)
        self.start_frame = 50
        self.end_frame = None
        self.offset = None
        self.dark_noise = None

    def get_offset_path(self, default_offset):
        """
        Creates the offset filepath using src_path and default_offset
        
        Returns: The full offset filepath
        """
        parent_dir = os.path.split(self.src_path)[0]
        return os.path.join(parent_dir, "lib", "Dark_Offset", default_offset)
        
    def get_noise_path(self, default_noise):
        """
        Creates the dark (read) noise filepath using src_path and default_noise
        
        Returns: The full dark (read) noise path
        """
        parent_dir = os.path.split(self.src_path)[0]
        return os.path.join(parent_dir, "lib", "Dark_Noise", default_noise)

    def load_default(self):
        """
        Loads the default offset and dark (read) noise from offset_filepath and
        noise_filepath. These are saved to self.offset and self.dark_noise
        respectively.        
        """
        self.get_noise()
        print("Loaded default offset from \"{}\"".format(self.offset_filepath))
        sleep(0.5)
        self.get_offset()
        print("Loaded default noise from \"{}\"".format(self.noise_filepath))
        sleep(0.5)

    def get_offset(self):
        """
        Reads pedestal values from filepath and updates Settings.pedestal

        Args:
            filepath: string, valid path to pedestal value
        """
        try:
            self.offset = np.load(self.offset_filepath)
        except:
            errorstatement = "Unable to find default offset, check if the file "
            errorstatement += "was deleted of lib directory was moved"
            raise ImportError(errorstatement)
        
    
    def get_noise(self):
        """
        Reads pedestal values from filepath and updates Settings.read_error

        Args:
            filepath: string, valid path to dark error values
        """
        try:
            self.dark_noise = np.load(self.noise_filepath)
        except:
            errorstatement = "Unable to find default noise, check if the file "
            errorstatement += "was deleted or lib directory was moved"
            raise ImportError(errorstatement)
        
    def check(self):
        """
        Checks that all settings attributes have the correct datatype.

        returns: prints error message if a setting is incorrect
        """
        issue_setting = None
        issue_type = None
        default_type = None

        try:
            if self.start_frame != None:
                int(self.start_frame)
        except:
            issue_setting = "start_frame"
            issue_type = type(self.start_frame)
            default_type = "<int>"

        try:
            if self.end_frame != None:
                int(self.end_frame)
        except:
            issue_setting = "end_frame"
            issue_type = type(self.end_frame)
            default_type = "<int>"
        
        if issue_setting != None:
            print("Settings error: {} must be type {}, not {}".format(issue_setting, default_type, issue_type))
