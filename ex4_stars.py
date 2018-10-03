#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

:Author: Georgios PAPADOPOULOS and Martin NOVOA
:Date:  14 February 2018

"""

import sys
import lib_args
import lib_wcs
import lib_cluster
import lib_fits
import matplotlib.pyplot as plt
import lib_background
import lib_stars
import ex3_clusters

def main():

    # analyse command line arguments

    file_name, interactive = lib_args.get_args()

    # importing image
    pixels = None
    pixels, header = lib_fits.read_first_image(file_name)
    my_wcs = lib_wcs.get_wcs(header)

    sorted_clusters = ex3_clusters.find_clusters(pixels, False)


    peak_pixel = lib_wcs.PixelXY(sorted_clusters[0].y,sorted_clusters[0].x)
    cel_coord = lib_wcs.xy_to_radec(my_wcs, peak_pixel)
    acc_radius = 0.001
    celestial_objects, out, req = lib_stars.get_celestial_objects(cel_coord, acc_radius)

    signature_fmt_1 = 'RESULT: right_ascension = {:.3f}'.format(cel_coord[0])
    signature_fmt_2 = 'RESULT: declination = {:.3f}'.format(cel_coord[1])
    print(signature_fmt_1)
    print(signature_fmt_2)
    i = 0
    for key in celestial_objects.keys():
        signature_fmt_3 = 'RESULT: celestial_object_{:d} = {}'.format(i, key)
        print(signature_fmt_3)
        i+=1

    # graphic output
    if interactive:
        # ...
        pass

    # end
    return 0


if __name__ == '__main__':

    sys.exit(main())
