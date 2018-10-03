def read_first_image(file_name):
    from astropy.io import fits
    with fits.open(file_name) as fits_data:
        return fits_data[0].data, fits_data[0].header




