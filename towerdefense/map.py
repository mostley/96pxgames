# -*- coding: utf8 -*- 

import sys, os, random
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.vector import *
from gamelib.librgb import *
from region import *

class Map:
    def __init__(self):
        self.towers = []
        self.heightData = []
        self.width = 100
        self.height = 100

        self.generateHeightMap()

    def generateHeightMap(self):
        for x in range(self.width):
            row = []
            for x in range(self.height):
                row.append(random.value)

            self.heightData.append(row)

    def update(self, dt):
        pass

    def draw(self, rgb):
        rgb.clear(BLACK)

        for region in self.regions:
            region.draw(rgb)

        for tower in self.towers:
            tower.draw(rgb)
