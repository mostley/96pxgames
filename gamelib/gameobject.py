# -*- coding: utf8 -*- 

from vector import *
from librgb import *

class GameObject:

	def __init__(self):
		self.position = Vector(0, 0)
		self.width = 1
		self.height = 1
		self.color = WHITE

	def update(self, dt):
		pass

	def draw(self, rgb):
		for x in range(self.width):
			for y in range(self.height):
				rgb.setPixel(self.position + Vector(x, y), self.color)