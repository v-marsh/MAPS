import numpy as np


class Settings():
    """
    Settings class for image analysis in the MAPS experiment

    Args:
        start_frame: int, the first frame of the run that is used for analysis
        end_frame: int, the final frame in the run that is used for analysis
    """
    offset_filepath = r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python\lib\Dark_Offset\Dark_test1"
    noise_filepath = r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python\lib\Dark_Noise\Dark_test1"
    resolution = (520, 520)
    start_frame = 50
    end_frame = None
    pedestal = None
    read_error = None

    def __init__(self):
        self.get_noise()
        self.get_offset()

    def get_offset(self):
        """
        Reads pedestal values from filepath and updates Settings.pedestal

        Args:
            filepath: string, valid path to pedestal value
        """
        self.pedestal = np.load(self.offset_filepath)
    
    def get_noise(self):
        """
        Reads pedestal values from filepath and updates Settings.read_error

        Args:
            filepath: string, valid path to dark error values
        """
        self.read_error = np.load(self.noise_filepath)
        
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
