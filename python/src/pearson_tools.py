import os
import numpy as np
from scipy.stats import chisquare
from scipy.stats import norm
from scipy.stats.contingency import expected_freq

ETS = "Pess <enter> to skip"

class Pearsontest():
    """
    Class for handling Peason's test on data against model functions
    """

    def __init__(self, chi2_arr=None):
        self.chi2_arr = chi2_arr

    def get_p_val(self):
        """
        Asks user to input confidence level for Pearson's cumulative test
        
        Returns: float; confidence level between 0 and 1, or None if the user
            chooses to skip (press enter)"""
        while True:
            print("Please enter confidence level for test as a", end=" ")
            print("probability between 0 and 1")
            print(ETS)
            confidence = input()
            if confidence == "":
                return None
            try:
                confidence = float(confidence)
            except:
                print("Error: confidence level must be between 0 and 1,", end=" ")
                print("not \"{}\"".format())
                continue
            if confidence > 1 or confidence < 0:
                print("Error: {} is not between 0 and 1".format(confidence))
                continue
            else:
                return confidence

    def get_ppb(self):
        """
        Asks user to input number of unique values per bin in std. input
        
        Returns: int; the number of unique values given in integer was inputted,
            None if <enter> was inputted
        """
        while True:
            print("Please enter the indeger number of unique values per bin")
            print(ETS)
            ppd = input()
            if ppd == "":
                return None
            try:
                ppd = int(ppd)
            except:
                print("Error: input must be an integer")
                continue
            if ppd <= 0:
                print("Error: must have at least values per bin")
                continue
            else:
                return ppd

    def gaussian(self, x_vals, loc, spread, sum=None):
        """
        Returns the x_vals when calculated for a gaussian with mean loc and
        std. dev. given by spread
        
        Args:
            x_vals: array_like; x values

            loc: float; mean
            
            spread: float; std. dev.

            sum: float; if set to a number then the discrete points will be 
                normalised so that they sum to that number. If set to None then
                nothing is done

        Returns:
            Array of gaussian values calculated for x_vals
        """
        g_val = np.exp(-1/2*np.square((x_vals-loc)/spread)) / (spread*np.sqrt(2*np.pi))
        g_sum= float(g_val.sum())
        if sum != None:
            norm = g_sum/sum
            g_val /= norm
        return g_val

    def run_test(self, data, resolution, ppb, model="gauss"):
        """
        Runs Pearson's chi-square test on data against a model distribution
        
        Args:
            data: array_like; data to run test on

            axis: int; axis to evaluate test over if data is a multidimensional
                array
            
            ppb: int; unique points per bin i.e. number of unique values in
                each bin.
            
            model: str; model function to test data against. Models are:
                gauss - gaussian function
        
        Returns: p value for Pearson's chi-sqaure test. If data is a
            multidimensional array then an array of p values are returned.
        """
        data = np.asarray(data, dtype=np.float64)
        loc = data.mean(axis=0)
        spread = data.std(axis=0)
        chi2_arr = np.zeros([2, *resolution], dtype=np.float64)
        for i in range(resolution[0]):
            for j in range(resolution[1]):
                # Create bin array with bins integer bins between max an min
                bin_edge = np.arange(np.min(data[:, i, j]) - 0.5, \
                    np.max(data[:, i, j]) + 0.5, step=ppb, dtype=float)
                # Determine bin probabilities
                bin_prob = np.histogram(data[:, i, j], \
                    bins=bin_edge, density=True)[0]
                # Determine empty bins
                non_empty = bin_prob.nonzero()
                # Remove empty bins
                bin_prob = bin_prob[non_empty]
                bin_mid = (bin_edge[non_empty] + 0.5).astype(int)
                df = len(bin_mid) - 2
                # NOTE: there is an issue with the gaussian function, it does
                # not calc the correct value! Try graphing them solution, must
                # calc mean and spread for specific dataset!
                expected_prob = self.gaussian(bin_mid, loc[i, j], spread[i, j],\
                    sum=bin_prob.sum())
                chi2_arr[0, i, j], chi2_arr[1, i, j] = chisquare(bin_prob,\
                    expected_prob, ddof=df)
                self.chi2_arr = chi2_arr
        return chi2_arr
    
    def save_chi2_arr(self, filepath):
        """
        Saves the loaded self.chi2_arr
        """
        if type(self.chi2_arr) != np.ndarray:
            print("Error: No chi2_arr saved, aborting!")
            return False
        elif os.path.isfile == True:
            print("Error: filepath is already in use, aborting!")
            return False
        else:
            with open(filepath, "wb") as f:
                np.save(f, self.chi2_arr)
            return True
    
    def run_cutoff(self, chi2_arr, resolution):
        """
        Ask user for cutoff value determines the number of pixel that don't pass

        Args:
            chi2_arr: array_like: array of chi2 values, outer dimension must equal 2,
                dim 0: chi2 values
                dim 1: p values

        Returns:
            Truth array of all cut pixels
        """
        p_val = self.get_p_val()
        # To allow user to exit
        if p_val == None:
            return None
        passed_pixels = chi2_arr[1] < p_val
        total_pix = resolution[0] * resolution[1]
        good_pix = np.count_nonzero(passed_pixels)
        bad_pix_abs = total_pix - good_pix
        bad_pix_rel = bad_pix_abs / total_pix
        print("Total number of pixels passed: {}".format(good_pix))
        print("Total number of pixels cut: {}".format(bad_pix_abs))
        print("Relative number of pixels cut: {}".format(bad_pix_rel))
        return passed_pixels
        


        



        

        # Check for dimensions of array.
        # calc array of pearsons cumulative test parameter
        # compare test parameter with chi square test over correct axis