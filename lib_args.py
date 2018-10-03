#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lib_args module"""

import argparse
import os
import sys


def get_default_data_path():
    # Etablish the default path and file values
    default_data_path = os.environ.get('DATAPATH')
    if default_data_path is None:
        if os.path.exists('../../data/fits'):
            default_data_path = '../../data/fits'
        elif os.path.exists('../data/fits'):
            default_data_path = '../data/fits'
        elif os.path.exists('../data'):
            default_data_path = '../data'
        else:
            sys.stderr.write('No default data path found!')
            exit(1)
    return default_data_path


def get_args():

    """Analyse the command line arguments using argparse"""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-b',
        dest='batch',
        action='store_true',
        default=False,
        help='batch mode, no graphics and no interaction')
    parser.add_argument('file', nargs='?', help='fits input file')
    args = parser.parse_args()

    if not args.file:
        # if no file name given on the command line
        default_data_file = 'common'
        if args.batch:
            data_file = default_data_file
        else:
            data_file = input('file name [%s]? ' % default_data_file)
            if not data_file:
                data_file = default_data_file
    else:
        data_file = args.file

    if not data_file.endswith('.fits'):
        # we need *.fits files
        data_file += '.fits'

    if data_file.rfind('/') == -1 and data_file.rfind('\\') == -1:
        # when an explicit path is not provided, prepend the default path
        data_file = get_default_data_path() + '/' + data_file

    if not os.path.exists(data_file):
        raise FileNotFoundError(
            'Image file ({}) not found'.format(data_file))

    # we don't test if the file actually exists.
    # thus we expect that this test will occur at open time (perhaps using a
    # try clause)

    return data_file, not args.batch


# =====
# Unit tests
# =====

if __name__ == '__main__':

    print(get_args())

    sys.exit(0)
