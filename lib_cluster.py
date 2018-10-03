import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import scipy.ndimage
import lib_background

def build_pattern(interactive):

    x = np.linspace(-4,4,9)
    y = np.linspace(-4,4,9)
    y = y[:, np.newaxis]
    pattern = gaussian2D(x, y, 1, 0, 9/4., 0, 9/4.)
    normPattern = pattern/pattern.sum().sum()
    if interactive:
        fig, main_axes = plt.subplots()
        main_axes.imshow(normPattern)
    return normPattern

def gaussian2D (x, y, norm, p1, p2, q1, q2):
    """
    compute a 2D gaussian function:
    """
    f = norm * np.exp( -(x - p1) ** 2 / (p2 ** 2) - (y - q1) ** 2 / (q2 ** 2) )

    return f

def extend(image, interactive,background, border_size):

    dimy, dimx = image.shape
    row = np.full((border_size,dimx),background)
    column = np.full((2*border_size + dimy,border_size), background)
    extended_im = np.append(row, np.append(image, row, axis=0), axis=0)
    extended_im = np.append(column, np.append(extended_im, column, axis=1), axis=1)

    if interactive:
        # Plot the extended image
        fig, main_axes = plt.subplots()
        main_axes.imshow(extended_im)

    return extended_im

def convolve(ext_image, pattern):
    return scipy.signal.convolve2d(ext_image, pattern, mode = 'valid')

def has_peak(conv_image, interactive, threshold):
    lm = scipy.ndimage.filters.maximum_filter(conv_image, size = 3, mode = 'constant', cval = 0)
    msk = (conv_image == lm) * (conv_image > threshold )
    if interactive:
        # Plot the extended image
        fig, main_axes = plt.subplots()
        main_axes.imshow(msk)
    return msk

def get_peaks_from_mask(max_mask):
    peaks = []
    for x in range(len(max_mask)):
        for y in range(len(max_mask[0])):
            if max_mask[x][y] == 1:
                peaks.append((x,y))
    return peaks

def get_clusters(peaks, image, threshold):

    clusters = []
    for peak in peaks:
        clusters.append(Cluster(peak[0],peak[1], image, threshold))
    return clusters

def get_int_lumi(x, y, radius, image):
    lumi = 0
    for i in range(x-(radius-1), x+radius):
        for j in range(y-(radius-1), y+radius):

            lumi += image[i][j]

    return lumi



class Cluster:
    def __init__(self, x, y, image, threshold):
        self.x = x
        self.y = y
        self.peak_lumi = image[x][y]
        self.int_lumi = image[x][y]
        self.radius = 1
        new_radius = 2
        new_int_lumi = get_int_lumi(x, y, new_radius, image)
        while ((new_int_lumi-self.int_lumi) / (8 * new_radius - 8)) > threshold:
            self.radius = new_radius
            self.int_lumi = new_int_lumi
            new_radius += 1
            new_int_lumi = get_int_lumi(x, y, new_radius, image)



    def __repr__(self):
        name = "coordinates: ({},{}) \nradius: {}\npeak lumi: {}\n" \
               "int luminosity: {} ".format(
                    self.x, self.y, self.radius, self.peak_lumi, self.int_lumi)
        return name

