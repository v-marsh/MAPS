import numpy as np
import matplotlib.pyplot as plt

import run_path_tools as rpt
import image_analysis_tools as iat
import ptc_tools as ptc


from settings import Settings

if __name__ == "__main__":
    print("------------------------------")
    # Import settings and check their values 
    settings = Settings()
    settings.check()
    while True:
        load = input("Load previous settings (y/n)?\n")
        if load.strip() == "y":
            settings.load_previous()
            break
        elif load.strip() == "n":
            break
        else:
            print("Error: did not recognise input")
    
    # Main loop
    while True:
    # Decide on program type
        print("Please decide on program type:\nPress <1> for single run analysis")
        print("Press <2> for multiple run analysis")
        prog_type = input("Press <enter> to exit\n")
        if prog_type == "1":  
            # Import data for run and create Run object
            run = rpt.get_run(start_frame=settings.start_frame)
            if run.success == False:
                print("Import failed, aborting")
                exit()
            if load == "n":
                while True:
                    recalc = input("Recalculate pedestal and error (y/n)?\n")
                    if recalc.strip() == "y":
                        recalc == True
                        break
                    if recalc.strip() == "n":
                        recalc == False
                        break
                    else: print("Error: did not recognise input \"{}\"".format(recalc))
                run.offset = iat.get_offset(run.frame_arr)
                run.err_dark = iat.get_noise(run.frame_arr)
            iat.check_gauss(run, opb=1)


            # run.frame_avg = iat.graph_mean(run.frame_arr, smooth=None)
            # iat.graph_pixel(run.frame_arr, (50, 500))

        elif prog_type == "2":
            settings.load_previous()
            # Inport multiple runs and create list of run objects
            run_series = rpt.get_multi_run(settings.start_frame)
            # Ask for sorting
            while True:
                print("Sort data against signal of individual pixels (y/n)?")
                print("Press <enter> to exit program")
                sorting = input()
                if sorting == "y":
                    sorting = True
                    break
                elif sorting == "n":
                    sorting = False
                    break
                elif sorting == "":
                    exit()
                else: 
                    print("Error: input not recognised please try again")
            ptc_data = ptc.get_ptc(run_series, settings.pedestal, settings.read_error, \
                settings.resolution, sort=sorting)
            # Generate different plots depending on user input
            while True:
                print("Plot PT curve (y/n)?")
                print("Press <enter> to exit program")
                repeat = input()
                if repeat == "":
                    exit()
                elif repeat == "y":
                    # ptc_data.flatten()
                    ptc.graph_ptc(ptc_data, log=True)
                    continue
                elif repeat == "n":
                    break
                else:
                    print("Error: \"{}\" is an invalid choice".format(repeat))
                    continue
        else:
            exit()