import lib_wcs
import lib_stars
def getcelcoord(cluster, wcs):
    peak_pixel = lib_wcs.PixelXY(cluster.y, cluster.x)
    return lib_wcs.xy_to_radec(wcs, peak_pixel)

