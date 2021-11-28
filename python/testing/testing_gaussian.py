import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    filepath = input("Please enter a filepath")
    arr = np.load(filepath)
    plt.imshow(arr[1])
    plt.show()