import numpy as np

fwpath = r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python_old\lib\Full_well\fullwell_3smooth_w4_ptc2"
readpath = r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python_old\lib\Read_noise\read_noise_3smooth_w4_ptc2"
savepath = r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python_old\lib\FPN_quality_w5"

offsetpath = r"C:\Users\vidar\OneDrive - University of Bristol\Documents\Uni_2021_2022\MAPS_experiment\code\python_old\lib\Dark_Offset\w5_offset.npy"
fpn = 56.681686220472685

# if __name__ == "__main__":
#     fw = np.load(fwpath)
#     read_noise = np.load(readpath)
#     dynamic_range = 20*np.log10(fw/read_noise)
#     with open(savepath, "wb") as file:
#         np.save(file, dynamic_range)

if __name__ == "__main__":
    offset = np.load(offsetpath)
    fpn_quality = fpn/offset
    with open(savepath, "wb") as file:
        np.save(file, fpn_quality)
