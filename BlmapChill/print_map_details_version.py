#!/usr/bin/env python
#
# prints the version field in the map details
#
# usage: python print_map_details_version.py BlmapChill.map
#
# expected sample output: 0184
#

from os.path import isfile
import sys

import twmap

if len(sys.argv) != 2:
    print(f"usage: {sys.argv[0]} map")
    sys.exit(0)

map_path = sys.argv[1]
if not isfile(map_path):
    print(f"Mapfile not found '{map_path}'", file=sys.stderr)
    exit(1)
m = twmap.Map(map_path)
print(m.info.version)
