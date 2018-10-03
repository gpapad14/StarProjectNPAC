#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

:Author: Georgios PAPADOPOULOS and Martin NOVOA
:Date:  15 February 2018

"""


import os
import sys
from matplotlib.widgets import RadioButtons
import matplotlib.pyplot as plt
import lib_fits

def main():
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.4)
    pixels, header = lib_fits.read_first_image("../data/common.fits")
    ax.imshow(pixels)
    my_widget_area = plt.axes([0.05, 0.4, 0.25, 0.3], facecolor= 'lightgoldenrodyellow')


    folder = list(os.walk("../data"))[0]
    dirpath, dirnames, filenames = folder
    radio = RadioButtons(my_widget_area, tuple(filenames))

    def my_action(label):

        pixels, header = lib_fits.read_first_image("../data/" + label)
        ax.imshow(pixels)


    radio.on_clicked(my_action)
    plt.show()





if __name__ == '__main__':

    sys.exit(main())
