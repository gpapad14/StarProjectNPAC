#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pixels module"""

import math


class PixelsSet():
    """A Pixels set class"""

    def __init__(self):
        """ construct an empty set """
        self.pixels = []

    def __str__(self):
        """ printable format """
        return "{} at {}, {}".format(self.get_integral(), *self.get_peak())

    def add(self, row, column, value):
        """ add a given pixel to the set """
        self.pixels.append((row, column, value))

    def get_len(self):
        """ return the number of pixels """
        return len(self.pixels)

    def get_integral(self):
        """ sum the values of all pixels """
        return sum([pixel[2] for pixel in self.pixels])

    def get_top(self):
        """ max value of all pixels """
        return max([pixel[2] for pixel in self.pixels])

    def get_center(self):
        """ bounding box center """
        rows, cols, values = zip(*self.pixels)
        row_center = (min(rows) + max(rows)) / 2.0
        col_center = (min(cols) + max(cols)) / 2.0
        return row_center, col_center

    def get_centroid(self):
        """ average row and col """
        nbpixels = len(self.pixels)
        if nbpixels == 0:
            return None, None
        rows, cols, _ = zip(*self.pixels)
        row_mean = sum(rows) / nbpixels
        col_mean = sum(cols) / nbpixels
        return row_mean, col_mean

    def get_weighted(self):
        """" weighted centroid """
        integral = self.get_integral()
        row_mean, col_mean = self.get_centroid()
        row_weighted = sum([pixel[2] * ((pixel[0] - row_mean) ** 2)
                            for pixel in self.pixels])
        col_weighted = sum([pixel[2] * ((pixel[1] - row_mean) ** 2)
                            for pixel in self.pixels])
        row_weighted = math.sqrt(row_weighted) / integral + row_mean
        col_weighted = math.sqrt(col_weighted) / integral + col_mean
        return row_weighted, col_weighted

    def get_peak(self):
        """ centroid of the pixels which have the max value """
        max_value = 0
        max_pixels = []
        for pixel in self.pixels:
            if pixel[2] > max_value:
                max_value = pixel[2]
                max_pixels = [pixel]
            elif pixel[2] == max_value:
                max_pixels.append(pixel)
        rows, cols, _ = zip(*max_pixels)
        nbpixels = len(max_pixels)
        row_mean = sum(rows) / nbpixels
        col_mean = sum(cols) / nbpixels
        return row_mean, col_mean


# =====
# Unit tests
# =====

if __name__ == '__main__':

    # PixelsSet

    ps = PixelsSet()

    # x,y
    # 1,3  2,3  3,3
    # 1,2  2,2  3,2
    #      2,1  3,1

    # val
    # 10   20   20
    # 10   20   20
    #      10   10

    ps.add(2, 1, 10)
    ps.add(3, 1, 10)
    ps.add(1, 2, 10)
    ps.add(2, 2, 20)
    ps.add(3, 2, 20)
    ps.add(1, 3, 10)
    ps.add(2, 3, 20)
    ps.add(3, 3, 20)

    print("center: {:.2f} {:.2f}".format(*ps.get_center()))
    print("centroid: {:.2f} {:.2f}".format(*ps.get_centroid()))
    print("weighted: {:.2f} {:.2f}".format(*ps.get_weighted()))
    print("peak: {:.2f} {:.2f}".format(*ps.get_peak()))
