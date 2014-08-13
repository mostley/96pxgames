# -*- coding: utf8 -*- 

import sys, os, time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.vector import *
from gamelib.gameobject import *
from gamelib.librgb import *
from gamelib.animation import *

class Car(GameObject):
	def __init__(self, position, color):
		GameObject.__init__(self)

		self.position = position
		self.startColor = self.color = color

		self.movementStack = []

		self.isHightlighted = False
		self.isActive = False

		self.lastSimulationFrame = time.time()
		self.simulationInterval = 0.25

		mutedColor = (self.color[0] * 0.5, self.color[1] * 0.5, self.color[2] * 0.5)
		self.colorAnimation = Animation( self.color, mutedColor, 0.25, AnimationLoopType.PingPong )

	def update(self, dt):
		GameObject.update(self, dt)

		self.colorAnimation.update(dt)

		if self.isActive and self.hasMovements():
			if (time.time() - self.lastSimulationFrame) > self.simulationInterval:
				movement = self.movementStack.pop()

				self.position += movement
				self.position = Vector(self.position.x % PIXEL_DIM_X, self.position.y % PIXEL_DIM_Y)

				self.lastSimulationFrame = time.time()

		if self.isHightlighted:
			self.color = self.colorAnimation.getValue()
		else:
			self.color = self.startColor

	def draw(self, rgb):
		GameObject.draw(self, rgb)

	def addMovement(self, movement):
		self.movementStack.insert(0, movement)

	def hasMovements(self): return len(self.movementStack) > 0

	def getNextPosition(self):
		movement = self.movementStack[-1]
		pos = self.position + movement
		pos = Vector(pos.x % PIXEL_DIM_X, pos.y % PIXEL_DIM_Y)
		return pos

	def collide(self, otherGameObject, direction):
		self.movementStack = [ ]
		