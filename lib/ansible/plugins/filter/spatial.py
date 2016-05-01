# (c) 2016, Patrick Dufour <pjdufour.dev@gmail.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

# Make coding more python3-ish
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.compat.six import iteritems, string_types

from ansible import errors

resolutions = [
    156543.03390000000945292413,
    78271.51695000000472646207,
    39135.75847500000236323103,
    19567.87923750000118161552,
    9783.93961875000059080776,
    4891.96980937500029540388,
    2445.98490468750014770194,
    1222.99245234375007385097,
    611.49622617187503692548,
    305.74811308593751846274,
    152.87405654296875923137,
    76.43702827148437961569,
    38.21851413574218980784,
    19.10925706787109490392,
    9.55462853393554745196,
    4.77731426696777372598,
    2.38865713348388686299,
    1.19432856674194343150,
    0.59716428337097171575,
    0.29858214168548585787,
    0.14929107084274292894,
    0.07464553542137146447]

def latlon(value):
    if value is None:
        return value

    latlon = None
    if isinstance(value, string_types):
        latlon = [float(strip(x)) for x in value.split(",")]
    if type(value) is list:
        latlon = [(x if isinstance(x, float) else float(strip(x))) for x in value]
    return latlon

def latlon_to_text(value):
    latlon = latlon(value)
    text = "{0:.4f},{1:.4f}".format(*latlon)
    return text

def bbox(value):
    if value is None:
        return value

    bbox = None
    if isinstance(value, string_types):
        bbox = [float(strip(x)) for x in value.split(",")]
    if type(value) is list:
        bbox = [(x if isinstance(x, float) else float(strip(x))) for x in value]
    return bbox

def bbox_to_wkt(value, srid="4326"):
    ''' return well-known text for a bounding box '''

    bbox = bbox(value)
    wkt = "SRID={srid};POLYGON(({0} {1},{0} {3},{2} {3},{2} {1},{0} {0}))".format(*bbox)
    return wkt

def bbox_to_text(value):
    bbox = bbox(value)
    text = "{0:.4f},{1:.4f},{2:.4f},{3:.4f}".format(*bbox)
    return text

def west(value):
    bbox = bbox(value)
    text = "{0:.4f}".format(bbox[0])
    return text

def south(value):
    bbox = bbox(value)
    text = "{0:.4f}".format(bbox[1])
    return text

def east(value):
    bbox = bbox(value)
    text = "{0:.4f}".format(bbox[2])
    return text

def north(value):
    bbox = bbox(value)
    text = "{0:.4f}".format(bbox[3])
    return text

def zoom_to_resolution(value):
    return resolutions[value] if value >= 0 and value < len(resolutions) else None;

def resolution_to_zoom(value):
    return resolutions.index(value) if value >= 0 and value < len(resolutions) else None;

class FilterModule(object):
    ''' Ansible spatial jinja2 filters '''

    def filters(self):
        return {
            # bounding box math
            'latlon': latlon
            'bbox': bbox,
            'bbox_to_wkt': bbox_to_wkt,
            'bbox_to_text': bbox_to_text,
            'west': west,
            'south': south,
            'east': east,
            'zoom_to_resolution': zoom_to_resolution,
            'resolution_to_zoom': resolution_to_zoom
        }
