import numpy as np
import matplotlib.pyplot as plt

import run_path_tools as rpt
import image_analysis_tools as iat
from settings import Settings

if __name__ == "__main__":
    # Import settings
    settings = Settings()
    
    while True:
        print("\n")
        run = rpt.get_run()
        if run.success == False:
            print("Run failed, aborting")
            exit()
        # run.frame_avg = iat.graph_mean(run.frame_arr, smooth=1)
        iat.graph_pixel(run.frame_arr, (50, 500))
