#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

:Author: Georgios PAPADOPOULOS and Martin NOVOA
:Date:  14 February 2018

"""


import sys
import lib_args
import lib_fits
import matplotlib.pyplot as plt
import numpy as np

from src import lib_background


def main():

    # analyse command line arguments
    file_name, interactive = lib_args.get_args()

    pixels = None
    pixels, header = lib_fits.read_first_image(file_name)

    background, dispersion, mx, hist_sum = lib_background.compute_background(pixels, interactive)

    test_gaussian = lib_background.modelling_function(
                        np.arange(-10.0, 10.0, 1.0), 1.0, 1.0, 1.0).sum()

    print('RESULT: test_gaussian = {:3f}'.format(test_gaussian))
    signature_hist = 'RESULT: histogram = {:5d}'.format(hist_sum)
    print(signature_hist)
    print('RESULT: background = {:d}'.format(int(background)))
    print('RESULT: dispersion = {:d}'.format(int(dispersion)))

    # graphic output
    if interactive:
        # ...
        pass

    # end
    return 0


if __name__ == '__main__':

    sys.exit(main())
