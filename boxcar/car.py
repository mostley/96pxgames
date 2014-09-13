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

		self.health = 100
		self.isDead = False

		self.movementStack = []
		self.trail = []

		self.isHightlighted = False
		self.isActive = False

		self.isInInputMode = False

		self.lastSimulationFrame = time.time()
		self.simulationInterval = 0.5

		mutedColor = Color.multiply(self.color, 0.5)
		self.colorAnimation = Animation( self.color, mutedColor, 0.25, AnimationLoopType.PingPong )

	def update(self, dt):
		GameObject.update(self, dt)

		if not self.isDead:
			self.colorAnimation.update(dt)

			if self.isActive and self.hasMovements():
				if (time.time() - self.lastSimulationFrame) > self.simulationInterval:
					movement = self.movementStack.pop()

					self.trail.append(self.position.clone())

					self.position += movement
					self.position = Vector(self.position.x % PIXEL_DIM_X, self.position.y % PIXEL_DIM_Y)

					self.lastSimulationFrame = time.time()

			if self.isHightlighted:
				self.color = self.colorAnimation.getValue()
			else:
				self.color = self.startColor

		self.color = Color.multiply(self.color, self.health/100.0)

		if self.health <= 0:
			self.isDead = True

	def draw(self, rgb):
		GameObject.draw(self, rgb)

		for dot in self.trail:
			rgb.setPixel(dot, self.color)

	def addMovement(self, movement):
		self.movementStack.insert(0, movement)

	def hasMovements(self): return len(self.movementStack) > 0

	def getNextPosition(self):
		pos = None
		if len(self.movementStack) > 0:
			movement = self.movementStack[-1]
			pos = self.position + movement
			pos = Vector(pos.x % PIXEL_DIM_X, pos.y % PIXEL_DIM_Y)
		return pos

	def collide(self, otherGameObject, direction):
		self.movementStack = []
		self.health -= 20
	
	def reset(self):
		self.isDead = False
		self.health = 100

	def setInputMode(self, value):
		self.isInInputMode = value
		if value:
			self.trail = []