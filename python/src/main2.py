import os

import numpy as np
import matplotlib as plt
import run_path_tools as rpt
from settings import Settings


SRC_LOC = r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python\src"
QTE = "Press <q> to exit program"
ETS = "Press <enter> to skip"


if __name__=="__main__":
# Set working directory to src, exit program if failed
    if os.getcwd() != SRC_LOC:
        try:
            os.chdir(SRC_LOC)
        except:
            raise ImportError("Could not find src directory at \"{}\""\
                    .format(SRC_LOC))
# Intial setup:
    prog_data = rpt.Prog_data()
    settings = Settings()
    settings.check()
    settings.src_path = SRC_LOC
    # Decide whether to load in previous offset and dark noise
    while True:
        print("Load in previous settings (y/n)?")
        print(QTE)
        load = input().strip()
        if load == "y":
            settings.load_previous(True)
            break
        elif load == "n":
            settings.load_previous(False)
            break
        elif load == "":
            exit()
        else:
            print("Error: did not recognise input please try again\n")
    
# Main program:
    while True:
        print("--------------------------------------------------------")
        prog_data.print_saved()
        print("Press <1> to input new run")
        print("Press <2> to remove a loaded run")
        print("Press <3> to analyse a loaded run")
        print(QTE)
        func_choice = input()
        print("\n")
        if func_choice == "1":
            pass
            print("Please enter one of the following:")
            print("The path to a single dataset run")
            print("The path to a run directory containing multiple datasets")
            print(ETS)
            run_path = input()
            if run_path == "":
                pass
            elif os.path.isfile(run_path) == True:
                print("Recieved path to a single dataset\n")
                run_name = rpt.get_run_name(prog_data)
                prog_data.saved_runs[run_name] = rpt.get_single_run(\
                    name=run_name, filepath=run_path,\
                    start_frame=settings.start_frame)
                print("Run \"{}\" successfully created".format(run_name))
            elif os.path.isdir(run_path) == True:
                print("Recived path to run directory\n")
                run_name = rpt.get_run_name(prog_data)
                prog_data.saved_runs[run_name] = rpt.get_multi_run(\
                    dirpath=run_path, start_frame=settings.start_frame)
                print("Run \"{}\" successfully created".format(run_name))
            else:
                print("Error: the path \"{}\" was not recognised, aborting!\n"\
                    .format(run_path))
                print("\n")
            
        elif func_choice == "2":
            prog_data.print_saved()
            print("Please choose run to delete")
            run_name = input()
            prog_data.del_run(run_name)
        
        elif func_choice == "3":
            print("Please choose one of the following options:")
            print("<1> ")
            pass
            # Choice of what actions to perform on current datasets
            # - Get mean
            # - Get offset
            # - Graph a single pixel over a single dataset
            # - Test fit of a pixel
            # - Create PTC curve
                # - Plot differnt values
                # - need to be able to delete ptc obect (save space)

        
        elif func_choice == "q":
            exit()
        
        else:
            print("Error: input \"{}{}\" was not recognised, please try again\n"\
                .format(func_choice, r"\n"))
        
    # ask to load a new dataset (create new run object)
    # ask to create multiple datasets
    #     this will only load the dataset, not calc any values!!!
    # ask what to do aftewards 
    
