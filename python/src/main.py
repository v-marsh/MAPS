import numpy as np
import matplotlib.pyplot as plt

import run_path_tools as rpt
import image_analysis_tools as iat
from settings import Settings

if __name__ == "__main__":
    print("------------------------------")
    # Import settings and check their values 
    settings = Settings()
    settings.check()
    
    # Main loop
    while True:
    # Decide on program type
        print("Please decide on program type:\nPress <1> for single run analysis")
        prog_type = input("\n Press <2> for multiple run analysis")
        if prog_type == 1:  
            # Import data for run and create Run object
            run = rpt.get_run()
            if run.success == False:
                print("Import failed, aborting")
                exit()

            run.frame_avg = iat.graph_mean(run.frame_arr, smooth=None)
            # iat.graph_pixel(run.frame_arr, (50, 500))

        if prog_type == 2:
            # Inport multiple runs and create list of run objects
            run_series = rpt.get_multi_run()
            
