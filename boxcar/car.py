# -*- coding: utf8 -*- 

import sys, os, time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.vector import *
from gamelib.gameobject import *
from gamelib.librgb import *

class Car(GameObject):
	def __init__(self, position, color):
		GameObject.__init__(self)

		self.position = position
		self.startColor = self.color = color

		self.movementStack = []

		self.lastBlink = time.time()
		self.blinkInterval = 0.25

		self.isHightlighted = False
		self.isActive = False

		self.lastSimulationFrame = time.time()
		self.simulationInterval = 0.25

	def update(self, dt):
		GameObject.update(self, dt)

		if self.isActive and self.hasMovements():
			if (time.time() - self.lastSimulationFrame) > self.simulationInterval:
				movement = self.movementStack.pop()

				self.position += movement
				self.position = Vector(self.position.x % PIXEL_DIM_X, self.position.y % PIXEL_DIM_Y)

				self.lastSimulationFrame = time.time()

		if self.isHightlighted:
			if (time.time() - self.lastBlink) > self.blinkInterval:
				if self.startColor == self.color:
					self.color = BLACK
				else:
					self.color = self.startColor
				self.lastBlink = time.time()
		else:
			self.color = self.startColor

	def draw(self, rgb):
		GameObject.draw(self, rgb)

	def addMovement(self, movement):
		self.movementStack.insert(0, movement)

	def hasMovements(self): return len(self.movementStack) > 0
