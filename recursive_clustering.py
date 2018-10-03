#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

:Author: Georgios PAPADOPOULOS and Martin NOVOA
:Date:  15 February 2018

"""

import sys
import lib_args
import matplotlib.pyplot as plt
import lib_fits
import numpy as np
import lib_background
import lib_pixels_set

class Cluster:
    def __init__(self, x, y, peak_lumi, int_lumi):
        self.x = x
        self.y = y
        self.peak_lumi = peak_lumi
        self.int_lumi = int_lumi



    def __repr__(self):
        name = "coordinates: ({},{}) \npeak lumi: {}\n" \
               "int luminosity: {} ".format(
                    self.x, self.y,  self.peak_lumi, self.int_lumi)
        return name

def recursive_search(i, j, data, done, cluster_pixels, threshold):
    x_lim, y_lim = data.shape
    to_search = [(i - 1, j),(i + 1, j),(i, j - 1), (i, j + 1)]
    for pair in to_search:
        x , y = pair
        if  x > 0 and x < x_lim and y > 0 and y < y_lim and not done[x][y]:
            done[x][y] = 1
            if data[x][y] > threshold:
                cluster_pixels.add(x, y, data[x][y])
                recursive_search(x, y, data, done, cluster_pixels, threshold)
    return

def main():


    file_name, interactive = lib_args.get_args()

    data = None
    data, header = lib_fits.read_first_image(file_name)
    done = np.zeros(data.shape)

    background, dispersion, mx, hist_sum = lib_background.compute_background(data, False)
    threshold = background + 6.*dispersion
    cluster_pix_list = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            if not done[i][j]:
                done[i][j] = 1
                if data[i][j] > threshold:
                    cluster_pixels = lib_pixels_set.PixelsSet()
                    cluster_pixels.add(i,j,data[i][j])
                    recursive_search(i, j,data, done, cluster_pixels, threshold)
                    if cluster_pixels.get_len() > 1 :
                        cluster_pix_list.append(cluster_pixels)

    print([str(cluster) for cluster in cluster_pix_list])


    if interactive:
        fig, main_axes = plt.subplots()
        main_axes.imshow(data)
        for cluster in cluster_pix_list:
            peak = cluster.get_peak()
            plt.scatter([peak[1]], [peak[0]])

        fig, main_axes = plt.subplots()
        main_axes.imshow(data)
        for cluster in cluster_pix_list:
            for pixel in cluster.pixels:
                plt.plot(pixel[1], pixel[0], 'rs', alpha=0.05)

        fig, main_axes = plt.subplots()
        main_axes.imshow(data)
        matrix = np.zeros(data.shape)
        for cluster in cluster_pix_list:
            for pixel in cluster.pixels:
                matrix[pixel[0], pixel[1]] = 1
        plt.contour(matrix)

        plt.show()

    return 0

if __name__ == '__main__':

    sys.exit(main())
