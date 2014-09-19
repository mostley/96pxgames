# -*- coding: utf8 -*- 

from vector import *
from librgb import *
from gameobject import *
from animation import *

class AnimatedGameObject(GameObject):

	def __init__(self, position, color1, color2, animationDuration=1, loop=AnimationLoopType.Loop, algorithm=AnimationAlgorithm.Linear):
		GameObject.__init__(self)
		self.position = position
		self.color = color1
		self.color1 = color1
		self.color2 = color2
		self.animation = Animation(color1, color2, animationDuration, loop, algorithm)

	def update(self, dt):
		GameObject.update(self, dt)

		self.animation.update(dt)
		self.color = self.animation.getValue()

	def draw(self, rgb):
		GameObject.draw(self, rgb)

		for x in range(self.width):
			for y in range(self.height):
				rgb.setPixel(self.position + Vector(x, y).toIntArr(), self.color)