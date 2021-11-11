import os
import numpy as np
from time import sleep

ETS = "Press <enter> to skip"
default_noise = "Dark_test1"
default_offset = "Dark_test1"
default_chi2 = "Chi2_Test2"
default_passed_pix = "Passed_Pix1"

class Settings():
    """
    Settings class for image analysis in the MAPS experiment

    Args:
        start_frame: int, the first frame of the run that is used for analysis
        end_frame: int, the final frame in the run that is used for analysis
    """
    def __init__(self, src_path, offset=default_offset, noise=default_noise, \
        chi2=default_chi2, passed_pix=default_passed_pix):
        self.src_path = src_path
        self.offset_filepath = self.get_offset_path(offset)
        self.noise_filepath = self.get_noise_path(noise)
        self.chi2_filepath = self.get_chi2_path(chi2)
        self.passed_pix_filepath = self.get_passed_path(passed_pix)
        self.resolution = (520, 520)
        self.start_frame = 50
        self.end_frame = None
        self.offset = None
        self.dark_noise = None
        self.chi2_vals = None
        self.passed_pix = None

    def ask_save(self, parameter):
        """
        Saves the parameter to lib

        Args:
            parameter: str; valid parameter to save valid parameters are
                - offset
                - dark_noise
                - chi2_vals
        """
        options = {"offset": (self.offset, )}
        

    def get_offset_path(self, offset_name):
        """
        Creates the offset filepath using src_path and default_offset
        
        Returns: The full offset filepath
        """
        offset_name = offset_name + ".npy"
        parent_dir = os.path.split(self.src_path)[0]
        return os.path.join(parent_dir, "lib", "Dark_Offset", offset_name)
        
    def get_noise_path(self, noise_name):
        """
        Creates the dark (read) noise filepath using src_path and default_noise
        
        Returns: The full dark (read) noise path
        """
        noise_name = noise_name + ".npy"
        parent_dir = os.path.split(self.src_path)[0]
        return os.path.join(parent_dir, "lib", "Dark_Noise", noise_name)

    def get_chi2_path(self, chi2_name):
        """
        Creates the chi2 value filepath using src_path and chi2_name
        
        Args:
            chi2_name: filename of to store chi2_values

        Returns: The full chi2 path
        """
        chi2_name = chi2_name + ".npy"
        parent_dir = os.path.split(self.src_path)[0]
        return os.path.join(parent_dir, "lib", "Chi2_Vals", chi2_name)

    def get_passed_path(self, passed_name):
        """
        Creates the passed pixels filepath using src_path and passed_name
        
        Args:
            passed_name: str; filename of to store passed pixels

        Returns: The full passed pixel path
        """
        passed_name = passed_name + ".npy"
        parent_dir = os.path.split(self.src_path)[0]
        return os.path.join(parent_dir, "lib", "Passed_Pix", passed_name)

    def new_chi2_path(self):
        """
        Asks user to input a chi2 filename in std. input and checks if it can be
        used to generate a chi2 filepath

        Returns: Valid chi2 filepath unless aborted by user
        """
        while True:
            print("Please choose a chi2 filename to save chi2 data")
            print(ETS)
            chi2_name = input()
            if chi2_name == "":
                return 
            chi2_path = self.get_chi2_path(chi2_name)
            if os.path.isfile(chi2_path) == True:
                print("Error: \"{}\" is already is use".format(chi2_path))
                continue
            else:
                return chi2_path

    def load_default(self):
        """
        Loads the default offset and dark (read) noise from offset_filepath and
        noise_filepath. These are saved to self.offset and self.dark_noise
        respectively.        
        """
        self.get_offset()
        print("Loaded default offset from \"{}\"".format(self.offset_filepath))
        sleep(0.5)
        self.get_noise()
        print("Loaded default noise from \"{}\"".format(self.noise_filepath))
        sleep(0.5)
        self.get_chi2()
        print("Loaded default chi2 from \"{}\"".format(self.chi2_filepath))
        sleep(0.5)
        # self.get_passed_pix()
        # print("Loaded default passed pixels from \"{}\"".format(self.offset_filepath))
        # sleep(0.5)



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
        """
        try:
            self.dark_noise = np.load(self.noise_filepath)
        except:
            errorstatement = "Unable to find default noise, check if the file "
            errorstatement += "was deleted or lib directory was moved"
            raise ImportError(errorstatement)
    
    def get_chi2(self):
        """
        Reads chi2 values from self.chi2_path into self.chi2_vals
        """
        try:
            self.chi2_vals = np.load(self.chi2_filepath)
        except:
            errorstatement = "Unable to find chi2 values, check if the file "
            errorstatement += "was deleted or lib directory was moved"
            raise ImportError(errorstatement)
    
    def get_passed_pix(self):
        """
        Reads passed pixel values from self.passed_path into self.passed_pix
        """
        try:
            self.passed_pix = np.load(self.passed_pix_filepath)
        except:
            errorstatement = "Unable to find passed pixels, check if the file "
            errorstatement += "was deleted or lib directory was moved"
            raise ImportError(errorstatement)

    def check_offset(self):
        """
        Returns: True if offset is a ndarry, otherwise returns False
        """
        off_type = type(self.offset)
        if off_type == np.ndarray:
            return True
        else:
            return False
    
    def check_dark_noise(self):
        """
        Returns: True if dark_noise is a ndarry, otherwise returns False
        """
        noise_type = type(self.dark_noise)
        if noise_type == np.ndarray:
            return True
        else:
            return False
    
    def check_all(self):
        """
        Checks dark noise and offset values
        
        Returns: True if both dark noise and offset are np.ndarrays, otherwise
            returns False
        """
        if self.check_dark_noise() == True \
            and self.check_offset() == True:
            return True
        else:
            return False
    
    def check_chi2(self):
        """
        Checks if chi2 data is loaded
        
        Returns: True if chi2_vals is a np.ndarray, False if not 
        """
        if type(self.chi2_vals) != np.ndarray:
            return False
        else:
            return True

        
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
