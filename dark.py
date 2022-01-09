#!/usr/bin/env python3
"""
    BlmapChill

    dark design by fokkonaut
"""

import sys
import twmap

if len(sys.argv) != 3:
    print("usage: dark.py IN_MAP OUT_MAP")
    sys.exit(0)


m = twmap.Map(sys.argv[1])

#unfr+grassm
m.groups[17].layers[1].color = (200, 200, 200, 255)

# Stone
m.groups[17].layers[2].color = (130, 130, 130, 255)

# Unhook
m.groups[17].layers[4].color = (130, 130, 130, 255)

# TXT+Deep (farm tiles)
m.groups[17].layers[5].color = (130, 130, 130, 255)

# BG
m.groups[1].layers[0].quads[0].colors = [(206, 136, 115, 255), (196, 101, 76, 255),
                                         (202, 168, 137, 255), (191, 154, 134, 255)]

m.save(sys.argv[2])
