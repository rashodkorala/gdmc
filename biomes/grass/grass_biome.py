#!/usr/bin/env python3

"""
Load and use a world slice.
"""

import sys

import numpy as np

from gdpc import __url__, Editor, Block, geometry
from gdpc.exceptions import InterfaceConnectionError, BuildAreaNotSetError
from gdpc.vector_tools import addY


# Create an editor object.
# The Editor class provides a high-level interface to interact with the Minecraft world.
editor = Editor()


# Check if the editor can connect to the GDMC HTTP interface.
try:
    editor.checkConnection()
except InterfaceConnectionError:
    print(
        f"Error: Could not connect to the GDMC HTTP interface at {editor.host}!\n"
        "To use GDPC, you need to use a \"backend\" that provides the GDMC HTTP interface.\n"
        "For example, by running Minecraft with the GDMC HTTP mod installed.\n"
        f"See {__url__}/README.md for more information."
    )
    sys.exit(1)


# Get the build area.
try:
    buildArea = editor.getBuildArea()
except BuildAreaNotSetError:
    print(
        "Error: failed to get the build area!\n"
        "Make sure to set the build area with the /setbuildarea command in-game.\n"
        "For example: /setbuildarea ~0 0 ~0 ~64 200 ~64"
        #~0 0 ~0 is the center of the build area.
        #~64 200 ~64 is the size of the build area. With 200 being the height. With ~ being the player.
    )
    sys.exit(1)


# Get a world slice.
#
# A world slice contains all kinds of information about a slice of the world, like blocks, biomes
# and heightmaps. All of its data is extracted directly from Minecraft's chunk format:
# https://minecraft.fandom.com/wiki/Chunk_format. World slices take a while to load, but accessing
# data from them is very fast.
#
# To get a world slice, you need to specify a rectangular XZ-area using a Rect object (the 2D
# equivalent of a Box). Box.toRect() is a convenience function that converts a Box to its XZ-rect.
#
# Note that a world slice is a "snapshot" of the world: any changes you make to the world after
# loading a world slice are not reflected by it.

print("Loading world slice...")
buildRect = buildArea.toRect()
worldSlice = editor.loadWorldSlice(buildRect)
print("World slice loaded!")


# Most of worldSlice's functions have a "local" and a "global" variant. The local variant expects
# coordinates relatve to the rect with which it was constructed, while the global variant expects
# absolute coorndates.


vec = addY(buildRect.center, 0)
print(f"Block at {vec}: {worldSlice.getBlock(vec - buildArea.offset)}")
print(f"Block at {vec}: {worldSlice.getBlockGlobal(vec)}")


# Heightmaps are an easy way to get the uppermost block at any coordinate. They are very useful for
# writing terrain-adaptive generator algorithms.
# World slices provide access to the heightmaps that Minecraft stores in its chunk format, so you
# get their computation for free.
#
# By default, world slices load the following four heightmaps:
# - "WORLD_SURFACE":             The top non-air blocks.
# - "MOTION_BLOCKING":           The top blocks with a hitbox or fluid.
# - "MOTION_BLOCKING_NO_LEAVES": Like MOTION_BLOCKING, but ignoring leaves.
# - "OCEAN_FLOOR":               The top non-air solid blocks.
#
# Heightmaps are loaded into 2D numpy arrays of Y coordinates.

print(f"Available heightmaps: {worldSlice.heightmaps.keys()}")

heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

print(f"Heightmap shape: {heightmap.shape}")



# Place walls of stone bricks on the perimeter of the build area, following the curvature of the
# terrain.

print("Placing walls...")


#build a wall

for point in buildRect.outline:
    
    height = heightmap[tuple(point - buildRect.offset)]
    
    for y in range(height, height + 7):
        # Place the first layer of blocks
        editor.placeBlock(addY(point, y), Block("mossy_stone_bricks"))
        
        # Place the second layer of blwocks
        editor.placeBlock(addY(point+1, y+2), Block("mossy_stone_bricks"))
        
        # Place the third layer of blocks
    




#build the center building
geometry.placeCylinder(editor,addY(buildRect.center, height), 30 , 10, Block("dark_oak_planks"), tube=True)
geometry.placeCylinder(editor,addY(buildRect.center, height+9), 28 , 1, Block("glowstone"), tube=True)
geometry.placeCylinder(editor,addY(buildRect.center, height+10), 22 , 5, Block("stone_bricks"))

geometry.placeCylinder(editor,addY(buildRect.center, height+15), 28 , 5, Block("dark_oak_planks"), tube=True)
geometry.placeCylinder(editor,addY(buildRect.center, height+19), 26 , 1, Block("glowstone"), tube=True)

geometry.placeCylinder(editor,addY(buildRect.center, height+20), 20 , 5, Block("stone_bricks"))

geometry.placeCylinder(editor,addY(buildRect.center, height+25), 26 , 5, Block("dark_oak_planks"), tube=True)
geometry.placeCylinder(editor,addY(buildRect.center, height+29), 24 , 1, Block("glowstone"), tube=True)

geometry.placeCylinder(editor,addY(buildRect.center, height+30), 18 , 5, Block("stone_bricks"))

geometry.placeCylinder(editor,addY(buildRect.center, height+35), 24 , 5, Block("dark_oak_planks"), tube=True)
geometry.placeCylinder(editor,addY(buildRect.center, height+39), 22 , 1, Block("glowstone"), tube=True)

geometry.placeCylinder(editor,addY(buildRect.center, height+40), 16 , 5, Block("stone_bricks"))

geometry.placeCylinder(editor,addY(buildRect.center, height+45), 22 , 5, Block("dark_oak_planks"), tube=True)
geometry.placeCylinder(editor,addY(buildRect.center, height+49), 20 , 1, Block("glowstone"), tube=True)

geometry.placeCylinder(editor,addY(buildRect.center, height+50), 14 , 5, Block("stone_bricks"))

geometry.placeCylinder(editor,addY(buildRect.center, height+55), 16 , 10, Block("dark_oak_planks"), tube=True)
geometry.placeCylinder(editor,addY(buildRect.center, height+65), 20 , 4, Block("stone_bricks"))
geometry.placeCylinder(editor,addY(buildRect.center, height+68), 18 , 1, Block("glowstone"), tube=True)

geometry.placeCylinder(editor,addY(buildRect.center, height+69), 16 , 4, Block("stone_bricks"))
geometry.placeCylinder(editor,addY(buildRect.center, height+73), 14, 4, Block("stone_bricks"))
geometry.placeCylinder(editor,addY(buildRect.center, height+77), 12 , 4, Block("stone_bricks"))
geometry.placeCylinder(editor,addY(buildRect.center, height+81), 10 , 4, Block("stone_bricks"))
geometry.placeCylinder(editor,addY(buildRect.center, height+85), 24 , 4, Block("stone_bricks"))




#Make small houses in the build area

import sys

import numpy as np
from glm import ivec2, ivec3

from gdpc import __url__, Editor, Block, geometry
from gdpc.exceptions import InterfaceConnectionError, BuildAreaNotSetError
from gdpc.vector_tools import Y, addY, dropY, line3D, circle, fittingCylinder


groundCenter = addY(buildRect.center+20, height)

#chose a random point in the build area
randomPoint = np.random.randint(0, buildRect.size, 2) + buildRect.offset

#place three blocks on top of each other, centered to eachother. The first block is 3x3 second is 5x5 and third is 2x2. on the ground
geometry.placeCuboidHollow(
    editor,
    groundCenter + ivec3(-1, 0, -1), # Corner 1
    groundCenter + ivec3(1,  2, 1), # Corner 2
    Block("spruce_log")
)


geometry.placeCuboidHollow(
    editor,
    groundCenter + ivec3(-3, 3, -3), # Corner 1
    groundCenter + ivec3(3,  8, 3), # Corner 2
    Block("mossy_stone_bricks")
)


#build roads out of the center of the build area

