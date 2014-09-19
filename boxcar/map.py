# -*- coding: utf8 -*- 

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.vector import *
from gamelib.librgb import *
from block import *

class Map:
    def __init__(self, blockfile):
        self.spawnpoints = []

        self.blocks = []
        self.loadFile(blockfile)

    def loadFile(self, blockfile):
        lines = []
        try:
            with open(blockfile) as f:
                lines = f.readlines()
        except Exception as e:
            print "loading block file: ",e

        print "loading map '", blockfile, "'"
        for line in lines:
            try:
                line = line.strip()
                if len(line) <= 0: continue
                if line[0] == "#": continue

                lineParts = line.split('|')
                if len(lineParts) < 3: continue

                x = int(lineParts[0].strip())
                y = int(lineParts[1].strip())
                blocktype = int(lineParts[2].strip())

                if x < 0: x = PIXEL_DIM_X + x
                if y < 0: y = PIXEL_DIM_Y + y

                block = Block(Vector(x, y), blocktype)
                if blocktype == BlockType.SpawnPoint:
                    self.spawnpoints.append(block)
                else:
                    self.blocks.append(block)
            except Exception as e:
                print "loading block file lines: ",e

    def update(self, dt):
        pass

    def draw(self, rgb, isActive):
        if not isActive:
            rgb.clear((50, 50, 50))
        else:
            rgb.clear(BLACK)

        for block in self.blocks:
            block.draw(rgb)

    def getBlockAt(self, position):
        result = None

        for block in self.blocks:
            if block.position == position: # todo proper intersection
                result = block

        return result
