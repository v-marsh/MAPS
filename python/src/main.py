import numpy
import matplotlib

import image_analysis_tools as iat
filepath = input("Input a valid filepath:")
image_arr = iat.file_t_arr(filepath)
iat.graph_mean(image_arr)