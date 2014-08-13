# -*- coding: utf8 -*- 

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.vector import *
from gamelib.librgb import *

class Map:
	def __init__(self):
		self.spawnpoints = [
			Vector(1,1), 
			Vector(PIXEL_DIM_X-2, 1),
			Vector(PIXEL_DIM_X-2, PIXEL_DIM_Y-2),
			Vector(1, PIXEL_DIM_Y-2)
		]

		self.blocks = [
			Vector( 5, 2),
			Vector( 6, 2),
			Vector( 5, 3),
			Vector( 6, 3),
			Vector( 5, 4),
			Vector( 6, 4),
			Vector( 5, 3),
			Vector( 6, 3),
			Vector( 4, 3),
			Vector( 7, 3),
			Vector( 4, 4),
			Vector( 7, 4),
			Vector( 5, 5),
			Vector( 6, 5),

			Vector(10, 3),
			Vector(10, 4),

			Vector( 1, 3),
			Vector( 1, 4),
			
			Vector( 5, 0),
			Vector( 6, 0),
			Vector( 5, 7),
			Vector( 6, 7),
		]

	def update(self, dt):
		pass

	def draw(self, rgb, isActive):
		if not isActive:
			rgb.clear((50, 50, 50))
		else:
			rgb.clear(BLACK)

		for i in range(len(self.blocks)):
			block = self.blocks[i]

			rgb.setPixel(block, GREEN)

	def getBlockAt(self, position):
		result = None

		for block in self.blocks:
			if block == position:
				result = block

		return result
