import os
import numpy as np
import matplotlib.pyplot as plt


class Chi2_Tests:
    def __init__(self):
        self.datasets = []
        self.passed_pixels = []


def run_cutoff(chi2_arr, p_val, resolution=(520, 520)):
        """
        Ask user for cutoff value determines the number of pixel that don't pass

        Args:
            chi2_arr: array_like: array of chi2 values, outer dimension must equal 2,
                dim 0: chi2 values
                dim 1: p values

        Returns:
            Truth array of all cut pixels
        """
        if not isinstance(p_val, (int, float)):
            return None
        failed_pixels = chi2_arr[1] < p_val
        total_pix = resolution[0] * resolution[1]
        bad_pix = np.count_nonzero(failed_pixels)
        good_pix_abs = total_pix - bad_pix
        good_pix_rel = good_pix_abs / total_pix
        print("Total number of pixels cut: {}".format(bad_pix))
        print("Total number of pixels passed: {}".format(good_pix_abs))
        print("Relative number of pixels passed: {}".format(good_pix_rel))
        return failed_pixels


resolution = (520, 520)

if __name__ == "__main__":
    chi2_runs = Chi2_Tests()
    # Ask to load new dataset
    while True:
        print("Load new test (y/n)?")
        test = input()
        if test in ("n", "y"):
            break
        else:
            continue
    # Ask for path to dataset
    while True:
        if test == "n":
            break
        print("Please input a valid filepath to a Chisquared dataset")
        print("Press <enter> to skip")
        path = input()
        if path == "":
            break
        if os.path.isfile(path):
            chi2_runs.datasets.append(np.load(path))

            # try:
            #     chi2_runs.datasets.append(np.load(path, allow_pickle=True))
            # except Exception:
            #     print(f"Error: unable to load file {path}, skipping")
            continue
        elif os.path.isdir(path):
            filenames = os.listdir(path)
            for filename in filenames:
                filepath = os.path.join(path, filename)
                try:
                    chi2_runs.datasets.append(np.load(filepath))
                except Exception:
                    print(f"Error: unable to load file {filepath}, skipping")
        else:
            print(f"Error: file '{path}' not found")
            continue
        # add dataset to saved
    # Determine p value
    while True:
        print("Please enter a cutoff p_value between 0 and 1")
        print("Press <q> to exit")
        p_val = input()
        if p_val == "q":
            exit()
        try:
            p_val = float(p_val)
            break
        except ValueError:
            print("Error: p_value must be a number")
    # Determine the number of pixels that are above some thyreashold p value
    all_failed_pixels = np.empty(resolution, dtype=bool)
    all_failed_pixels.fill(True)
    for dataset in chi2_runs.datasets:
        all_failed_pixels = np.logical_and(all_failed_pixels, run_cutoff(dataset, p_val))
    # display truth array
    plt.imshow(all_failed_pixels.astype(int))
    plt.show()           