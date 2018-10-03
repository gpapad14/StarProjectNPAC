import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as sp

def compute_background(array2D, interactive):
    array1D = array2D.ravel()
    bin_number = 200
    bin_values, bin_boundaries = np.histogram(array1D, bin_number)

    # normalize the distribution for the gaussian fit
    my = np.float(np.max(bin_values))
    normal_y = bin_values / my
    mx = np.float(np.max(bin_boundaries))
    normal_x = bin_boundaries[:-1] / mx

    fit, covariant = sp.curve_fit(modelling_function, normal_x, normal_y)
    maxvalue = fit[0] * my
    background = fit[1] * mx
    dispersion = fit[2] * mx
    x = normal_x * mx
    y = normal_y * my
    if interactive:
        fig, axis = plt.subplots()
        plt.plot(x, y, 'b+:', label='data')
        plt.plot(x, modelling_function(x, maxvalue, background, dispersion), 'r-', label='fit')

        plt.legend()
        axis.set_title('Flux distribution')
        axis.set_xlabel('Amplitude')
        axis.set_ylabel('Frequency')
        plt.show()
    hist_sum = bin_values.sum()

    return background, dispersion, mx, hist_sum


def modelling_function(x, p1, p2, p3):
    """
    compute a gaussian function:
    """
    y = p1 * np.exp(-(x - p2)**2 / (2 * p3**2))

    return y