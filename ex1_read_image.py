#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

:Author: Georgios PAPADOPOULOS and Martin NOVOA
:Date:  14 February 2018

"""



import sys
import lib_args
import matplotlib.pyplot as plt
import lib_fits

def main():

    # analyse command line arguments

    file_name, interactive = lib_args.get_args()

    pixels = None
    pixels, header = lib_fits.read_first_image(file_name)

    signature_fmt_1 = 'RESULT: cd1_1 = {:.10f}'.format(header["CD1_1"])
    signature_fmt_2 = 'RESULT: cd1_2 = {:.10f}'.format(header["CD1_2"])
    signature_fmt_3 = 'RESULT: cd2_1 = {:.10f}'.format(header["CD2_1"])
    signature_fmt_4 = 'RESULT: cd2_2 = {:.10f}'.format(header["CD2_2"])

    print(signature_fmt_1)
    print(signature_fmt_2)
    print(signature_fmt_3)
    print(signature_fmt_4)


    if interactive:
        fig, main_axes = plt.subplots()
        main_axes.imshow(pixels)
        plt.show()

    return 0

if __name__ == '__main__':

    sys.exit(main())
