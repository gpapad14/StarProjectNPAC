#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

:Author: Georgios PAPADOPOULOS and Martin NOVOA
:Date:  15 February 2018

"""

import sys
import lib_args
import lib_wcs
import lib_stars
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import lib_fits
import lib_stars
import ex3_clusters

class Handler:
    def __init__(self, fig, axis, wcs):
        self.fig = fig
        self.axis = axis
        self.wcs = wcs
        self.texts = []
        self.patches = []
    """
    def move(self, event):
        x = event.xdata
        y = event.ydata
        return
    """

    def on_click(self, event):
        if event.button == 1:
            # Create a transformation matrix
            axis=event.inaxes
            for txt in self.texts:
                txt.remove()
            for patch in self.patches:
                patch.remove()
            self.texts = []
            self.patches = []
            display_to_image = axis.transData.inverted()
            # Image coordinates returned as a list
            image_x_y = display_to_image.transform((event.x, event.y))
            peak_pixel = lib_wcs.PixelXY(*image_x_y)
            cel_coord = lib_wcs.xy_to_radec(self.wcs, peak_pixel)
            #text = axis.text(*image_x_y, str(cel_coord[0]) + "\n" + str(cel_coord[1]), fontsize=10, color='white')
            acc_radius = 0.001
            celestial_objects, out, req = lib_stars.get_celestial_objects(cel_coord, acc_radius)

            for i, key in enumerate(celestial_objects.keys()):
                patch = axis.add_patch(patches.Rectangle(image_x_y-5,
                                 10,
                                 10,
                                 fill=False,
                                 color='white'
                                 )

                )

                text = axis.text(image_x_y[0]+6, image_x_y[1]- i * 5, key, fontsize=10, color='white')
                self.patches.append(patch)
                self.texts.append(text)
                print(key)


            event.canvas.draw()

        return


def main():

    file_name, interactive = lib_args.get_args()

    # importing image
    pixels = None
    pixels, header = lib_fits.read_first_image(file_name)
    my_wcs = lib_wcs.get_wcs(header)
    clusters = ex3_clusters.find_clusters(pixels, False)

    for j in range(len(clusters)):
        peak_pixel = lib_wcs.PixelXY(clusters[j].y, clusters[j].x)
        cel_coord = lib_wcs.xy_to_radec(my_wcs, peak_pixel)
        acc_radius = 0.001
        celestial_objects, out, req = lib_stars.get_celestial_objects(cel_coord, acc_radius)

        signature_fmt_1 = 'RESULT: right_ascension_{:d} = {:.3f}'.format(j, cel_coord[0])
        signature_fmt_2 = 'RESULT: declination_{:d} = {:.3f}'.format(j, cel_coord[1])
        print(signature_fmt_1)
        print(signature_fmt_2)
        for i, key in enumerate(celestial_objects.keys()):
            signature_fmt_3 = 'RESULT: celestial_object_{:d}_{:d} = {}'.format(j, i, key)
            print(signature_fmt_3)




    # graphic output
    if interactive:
        fig, main_axes = plt.subplots()
        handler = Handler(fig, main_axes, my_wcs)
        main_axes.imshow(pixels)
        #fig.canvas.mpl_connect('motion_notify_event', handler.move)
        fig.canvas.mpl_connect('button_press_event', handler.on_click)

        plt.show()




    # end
    return 0


if __name__ == '__main__':

    sys.exit(main())
