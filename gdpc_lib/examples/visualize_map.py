#!/usr/bin/env python3

"""A script that displays a map of the build area."""

import cv2
import matplotlib.pyplot as plt
import numpy as np

from gdpc import Editor, lookup


if __name__ == '__main__':
    editor = Editor()

    # see if a different build area was defined ingame
    buildArea = editor.getBuildArea()
    buildRect = buildArea.toRect()
    x1, z1 = buildRect.begin
    x2, z2 = buildRect.end

    # load the world data and extract the heightmap(s)
    worldSlice = editor.loadWorldSlice(buildRect)

    heightmap = np.array(worldSlice.heightmaps["OCEAN_FLOOR"], dtype=int)

    # calculate the gradient (steepness)
    decrementor = np.vectorize(lambda a: a - 1)
    cvheightmap = np.clip(decrementor(heightmap), 0, 255).astype(np.uint8)
    gradientX = cv2.Scharr(cvheightmap, cv2.CV_16S, 1, 0)
    gradientY = cv2.Scharr(cvheightmap, cv2.CV_16S, 0, 1)

    # create a dictionary mapping block ids ("minecraft:...") to colors
    palette = lookup.BLOCK_TO_COLOR

    # create a 2d map containing the surface block colors
    topcolor = np.zeros(buildRect.size, dtype='int')
    unknownBlocks = set()

    for x, z in buildRect.inner:
        # check up to 5 blocks below the heightmap
        for dy in range(5):
            # calculate absolute coordinates
            y = int(heightmap[(x - x1, z - z1)]) - dy

            block = worldSlice.getBlockGlobal((x,y,z))
            if block.id in lookup.MAP_TRANSPARENT:
                # transparent blocks are ignored
                continue

            if block.id not in palette:
                # unknown blocks remembered for debug purposes
                unknownBlocks.add(block.id)
            else:
                topcolor[(x - x1, z - z1)] = palette[block.id]
            break

    if len(unknownBlocks) > 0:
        print("Unknown blocks: " + str(unknownBlocks))

    # separate the color map into three separate color channels
    topcolor = cv2.merge(((topcolor) & 0xff, (topcolor >> 8)
                          & 0xff, (topcolor >> 16) & 0xff))

    # calculate a brightness value from the gradient
    brightness = np.expand_dims((gradientX + gradientY).astype("int"), 2)
    brightness = brightness.clip(-64, 64)

    topcolor += brightness
    topcolor = topcolor.clip(0, 256)

    # display the map
    topcolor = topcolor.astype('uint8')
    topcolor = np.transpose(topcolor, (1, 0, 2))
    plt_image = cv2.cvtColor(topcolor, cv2.COLOR_BGR2RGB)

    plt.imshow(plt_image)
    plt.show()
