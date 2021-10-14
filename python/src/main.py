import numpy
import matplotlib

import run_path_tools as rpt
import image_analysis_tools as iat


if __name__ == "__main__":
    run_setup = rpt.get_run()
    run_name = input("Input name of run, press <enter> to skip:")
    if run_name == "\n":
        run_name = None
    filepath = input("Input a valid filepath:")
    image_arr = iat.file_t_arr(filepath)
    iat.graph_mean(image_arr)