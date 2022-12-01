#!/usr/bin/env python3
"""
    patch_gen.py

    Given two teeworlds maps
    create a twmap script that describes
    the difference between the two

    so it can be applied like a patch
"""

import sys
import os
import numpy
import re
import twmap

def diff_layers(layer1, layer2):
    diffs = []
    if layer1.width() != layer2.width():
        print('Error: Layers of different width are not supported')
        sys.exit(1)
    if layer1.height() != layer2.height():
        print('Error: Layers of different height are not supported')
        sys.exit(1)
    for (y, x, flags), tile in numpy.ndenumerate(layer1.tiles):
        if flags != 0:
            # TODO: support flag diffs
            continue
        cmp_tile = layer2.tiles[y][x]
        # print('##')
        # print(f"x={x} y={y} tile={tile} cmp={cmp_tile[0]}")
        if tile == cmp_tile[0]:
            # skip matches
            continue
        diffs.append({
            'x': x,
            'y': y,
            'flags': cmp_tile[1],
            'tile': cmp_tile[0]})
    return diffs

def gen_py_layer_diff(diffs, layer, name):
    """
    Given a array of tile diffs
    this generats a python patches
    """
    patches = []
    layer_slug = re.sub(r'[^a-zA-Z_]', '', name)
    patches.append(f"{layer_slug} = in_map.{layer}.tiles")
    for diff in diffs:
        x = diff['x']
        y = diff['y']
        tile = diff['tile']
        flags = diff['flags']
        patches.append(f"{layer_slug}[{y}][{x}] = [{tile}, {flags}]")
        # print(diff
    patches.append(f"in_map.{layer}.tiles = {layer_slug}")
    return patches

def gen_py_patch(base_map_file, diff_map_file):
    """
    Given two map file paths
    this generats a python patch script
    that can be applied to the first map
    to get the second map
    """
    base_map = twmap.Map(base_map_file)
    diff_map = twmap.Map(diff_map_file)
    mapname = os.path.splitext(os.path.basename(base_map_file))[0]
    mapname = re.sub(r'[^a-zA-Z_]', '', mapname)
    diffname = os.path.splitext(os.path.basename(diff_map_file))[0]
    diffname = re.sub(r'[^a-zA-Z_]', '', diffname)
    if diffname.startswith(f"{mapname}_"):
        diffname = diffname[(len(mapname) + 1):]
    elif diffname.startswith(mapname):
        diffname = diffname[len(mapname):]
    patches = []
    patches.append('#!/usr/bin/env python3')
    patches.append('import twmap')
    patches.append(f"in_map = twmap.Map('{mapname}.map')")

    group_index = -1
    for group in base_map.groups:
        group_index += 1
        layer_index = -1
        for layer in group.layers:
            layer_index += 1
            print(f"name={layer.name} g={group_index} l={layer_index}")
            if layer.kind() not in ['Tiles', 'Game']:
                # TODO: support quads etc
                print(f"Warning: skipping {layer.kind()}")
                continue
            diffs = diff_layers(
                    base_map.groups[group_index].layers[layer_index],
                    diff_map.groups[group_index].layers[layer_index])
            patches += gen_py_layer_diff(
                    diffs,
                    f"groups[{group_index}].layers[{layer_index}]",
                    f"{group.name}_{layer.name}")

    patches.append(f"in_map.save('{mapname}.map')")

    patchfile = f"{mapname}_{diffname}_patch.py"
    with open(patchfile, 'w') as patch:
        patch.write("\n".join(patches) + "\n")
    os.chmod(patchfile, 0o744)

if len(sys.argv) != 3:
    print("usage: patch_gen.py BASE_MAP DIFF_MAP")
    sys.exit(0)

base_map_file = sys.argv[1]
diff_map_file = sys.argv[2]
gen_py_patch(base_map_file, diff_map_file)
