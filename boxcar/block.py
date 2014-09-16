# -*- coding: utf8 -*- 

from gamelib.gameobject import *
from gamelib.color import *

class BlockType:
	SpawnPoint = 0
	Gras = 1
	Fire = 2
	HWalker = 3
	VWalker = 4

class Block(GameObject):

	def __init__(self, position, blocktype):
		GameObject.__init__(self)

		self.position = position
		self.blocktype = blocktype

		if self.blocktype == BlockType.Gras:
			self.color = GREEN
		elif self.blocktype == BlockType.Fire:
			self.color = RED
		elif self.blocktype == BlockType.HWalker:
			self.color = YELLOW
		elif self.blocktype == BlockType.VWalker:
			self.color = PURPLE

	def draw(self, rgb):
		if self.blocktype != BlockType.SpawnPoint:
			GameObject.draw(self, rgb)