#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Utilities for SIMBAD access
"""


import sys
import time
import urllib.request
import urllib.error
import urllib.parse
import collections


RADIUS = 0.001


def make_req(radec, radius):
    """
    Build a request to the Simbad server
    :param radec: floating point value of the (RA,DEC) coordinate
    :param radius: floting value of the acceptance radius (degrees)
    :return: request text
    """

    def crep(text, char):
        """
        :param text: string which must be modified
        :param char: character to be replaced
        :return:
        """
        text = text.replace(char, '%%%02X' % ord(char))
        return text

    host_simbad = 'simbad.u-strasbg.fr'

    # WGET with the "request" string built as below :

    script = ''
    # output format (for what comes from SIMBAD)
    script += 'format object f1 "'
    script += '%COO(A)'  # hour:minute:second
    script += '\t%COO(D)'  # degree:arcmin:arcsec
    script += '\t%OTYPE(S)'
    script += '\t%IDLIST(1)'
    script += '"\n'

    script += 'query coo '
    script += '%f' % radec.ra  # append "a_ra" (decimal degree)
    script += ' '
    script += '%f' % radec.dec  # append "a_dec" (decimal degree)
    script += ' radius='
    script += '%f' % radius  # append "a_radius" (decimal degree)
    script += 'd'  # d,m,s
    script += ' frame=FK5 epoch=J2000 equinox=2000'  # fk5
    script += '\n'

    # "special characters" converted to "%02X" format :
    script = crep(script, '%')
    script = crep(script, '+')
    script = crep(script, '=')
    script = crep(script, ';')
    script = crep(script, '"')
    script = crep(script, ' ')  # same as upper line.

    script = script.replace('\n', '%0D%0A')  # CR+LF
    script = crep(script, '\t')

    request = 'http://' + host_simbad + '/simbad/sim-script?'
    request += 'script=' + script + '&'

    return request


def wget(req):
    """
    :param req:
    :return:
    """
    retry = 0
    result = None

    while retry < 10:
        # pylint: disable=broad-except
        try:
            result = urllib.request.urlopen(req)
            break
        except urllib.error.HTTPError:
            retry += 1
            time.sleep(0.2)
        except BaseException:
            raise

        sys.stderr.write(
            'Retrying to read {} ({} attempts remaining)'.format(
                req, retry))

    if result is None:
        return None

    try:
        text = result.read()
        text = text.decode("utf-8")
        lines = text.split('<BR>\n')
        return lines[0]
    except Exception:
        sys.stderr.write('cannot read URL {}'.format(req))
    except BaseException:
        raise


def get_celestial_objects(object_radec, radius=RADIUS):
    """
    Provide celestial objects.
    """

    req = make_req(object_radec, radius)
    out = wget(req)
    if out is None:
        return '', out, req

    out = out.split('\n')
    in_data = False
    raw_objects = dict()

    for line in out:
        line = line.strip()
        if line == '':
            continue
        if not in_data:
            if line == '::data::' + '::' * 36:
                in_data = True
            continue

        data = line.split('\t')
        obj_name = data[3].strip()
        obj_type = data[2].strip()
        # if  obj_type!='Unknown' and obj_type!='HII':
        if obj_type != 'HII':
            raw_objects[obj_name] = obj_type

    objects = collections.OrderedDict(sorted(raw_objects.items()))

    return objects, out, req


# =====
# Unit tests
# =====

if __name__ == '__main__':

    class RaDec:
        """Spatial coordinates."""

        def __init__(self):
            """ Initializing """
            self.ra = 0.0
            self.dec = 0.0

    radec = RaDec()
    radec.ra, radec.dec = 1.0, 1.0
    cobjects, _, _ = get_celestial_objects(radec, 0.1)
    for cobj_name in sorted(cobjects.keys()):
        print(cobj_name)
