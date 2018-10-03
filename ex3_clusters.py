#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

:Author: Georgios PAPADOPOULOS and Martin NOVOA
:Date:  14 February 2018

"""

import sys
import lib_args
import lib_cluster
import lib_fits
import matplotlib.pyplot as plt
import lib_background

def find_clusters(pixels, interactive):
    pattern = lib_cluster.build_pattern(interactive)
    background, dispersion, mx, hist_sum = lib_background.compute_background(pixels, interactive)
    threshold = background + 6. * dispersion
    extended_image = lib_cluster.extend(pixels, interactive, 0, 4)
    convolved_image = lib_cluster.convolve(extended_image, pattern)
    max_mask = lib_cluster.has_peak(convolved_image, interactive, threshold)
    peak_list = lib_cluster.get_peaks_from_mask(max_mask)
    clusters = lib_cluster.get_clusters(peak_list, pixels, threshold)
    sorted_clusters = sorted(clusters, key=lambda cluster: -cluster.int_lumi)
    return sorted_clusters


def main():

    # analyse command line arguments
    file_name, interactive = lib_args.get_args()

    # importing image
    pixels = None
    pixels, header = lib_fits.read_first_image(file_name)

    pattern = lib_cluster.build_pattern(interactive)

    background, dispersion, mx, hist_sum = lib_background.compute_background(pixels, interactive)
    threshold = background + 6. * dispersion

    extended_image = lib_cluster.extend(pixels, interactive, 0, 4)
    convolved_image = lib_cluster.convolve(extended_image, pattern)
    extended_convolved_image = lib_cluster.extend(convolved_image, interactive, 0, 1)

    max_mask = lib_cluster.has_peak(convolved_image, interactive, threshold)
    peak_list = lib_cluster.get_peaks_from_mask(max_mask)
    clusters = lib_cluster.get_clusters(peak_list, pixels, threshold)
    sorted_clusters = sorted(clusters, key=lambda cluster: -cluster.int_lumi)




    print('RESULT: pattern_sum = {:5.0f}'.format(pattern.sum().sum()))

    print('RESULT: extended_image_width = {:2d}'.format(extended_image.shape[0]))
    print('RESULT: extended_image_height = {:2d}'.format(extended_image.shape[1]))
    print('RESULT: extended_image_sum = {:5.0f}'.format(extended_image.sum().sum()))

    print('RESULT: convolution_image_width = {:2d}'.format(convolved_image.shape[0]))
    print('RESULT: convolution_image_height = {:2d}'.format(convolved_image.shape[1]))
    print('RESULT: convolution_image_sum = {:5.0f}'.format(convolved_image.sum().sum()))

    print('RESULT: extended_convolution_image_width = {:2d}'.format(extended_convolved_image.shape[0]))
    print('RESULT: extended_convolution_image_height = {:2d}'.format(extended_convolved_image.shape[1]))
    print('RESULT: extended_convolution_image_sum = {:5.0f}'.format(extended_convolved_image.sum().sum()))

    print('RESULT: peaks_number={:2d}'.format(max_mask.sum().sum()))

    print('RESULT: clusters_number={:2d}'.format(len(sorted_clusters)))
    print('RESULT: cluster_max_top={:5d}'.format(int(sorted_clusters[0].peak_lumi)))

    print('RESULT: cluster_max_integral={:5d}'.format(int(sorted_clusters[0].int_lumi)))
    print('RESULT: cluster_max_column={:5d}'.format(int(sorted_clusters[0].y)))
    print('RESULT: cluster_max_row={:5d}'.format(int(sorted_clusters[0].x)))

    # graphic output
    if interactive:
        fig, main_axes = plt.subplots()
        main_axes.imshow(convolved_image)
        #plt.show()


    # end
    return 0


if __name__ == '__main__':

    sys.exit(main())
