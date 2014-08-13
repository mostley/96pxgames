# -*- coding: utf8 -*- 

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.vector import *
from gamelib.librgb import *

class Map:
	def __init__(self):
		self.spawnpoints = [
			Vector(0,0), 
			Vector(PIXEL_DIM_X-1, 0),
			Vector(PIXEL_DIM_X-1, PIXEL_DIM_Y-1),
			Vector(0, PIXEL_DIM_Y-1)
		]

	def update(self, dt):
		pass

	def draw(self, rgb, isActive):
		if not isActive:
			rgb.clear(BLACK)
		else:
			rgb.clear((50, 50, 50))