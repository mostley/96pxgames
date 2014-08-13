#!/usr/bin/python
# -*- coding: utf8 -*- 

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.game import *
from car import *
from map import *
from explosion import *

class GameMode:
	Bootstrap = 0
	PlayerInput = 1
	Simulate = 2

class BoxCar(Game):

	def __init__(self, ip):
		Game.__init__(self, ip)

		self.map = Map()
		carColors = [ORANGE, BLUE, TURQUE, YELLOW]

		self.cars = [Car(self.map.spawnpoints[i], carColors[i]) for i in range(self.playerCount)]

		self.currentPlayer = 0
		self.mode = GameMode.Bootstrap

		self.setMode(GameMode.Bootstrap)

		self.sprites = []

	def simulationIsOver(self):
		result = True

		for car in self.cars:
			if car.hasMovements():
				result = False
				break

		return result

	def setMode(self, mode):
		if self.mode != mode:
			self.mode = mode

			if self.mode == GameMode.PlayerInput:
				self.currentPlayer = 0
				print "PlayerInput Mode"
			elif self.mode == GameMode.Simulate:
				self.currentPlayer = 0
				#self.lastSimulationFrame = time.time()
				print "Simulation Mode"
			elif self.mode == GameMode.Bootstrap:
				print "Bootstrap Mode"
			else:
				print "Unknown Mode"

	def nextPlayer(self):
		self.currentPlayer += 1

		if self.currentPlayer >= self.playerCount:
			self.setMode(GameMode.Simulate)

	def update(self, dt):

		if self.mode == GameMode.Simulate:
			if self.simulationIsOver():
				self.setMode(GameMode.PlayerInput)
		elif self.mode == GameMode.PlayerInput:
			Game.update(self, dt)
		else:
			self.setMode(GameMode.PlayerInput)
		
		self.map.update(dt)

		for player in range(len(self.cars)):
			car = self.cars[player]

			car.isActive = self.mode == GameMode.Simulate
			car.isHightlighted = self.mode == GameMode.PlayerInput and self.currentPlayer == player

			self.collisionHandling(car)
			car.update(dt)

		self.sprites = [sprite for sprite in self.sprites if not sprite.isDead]
		for sprite in self.sprites:
			sprite.update(dt)

	def collisionHandling(self, car):
		if car.isActive and car.hasMovements():
			nextPos = car.getNextPosition()
			direction = nextPos - car.position

			block = self.map.getBlockAt(nextPos)
			if block != None:
				car.collide(block, direction)
				self.addExplosion(car.position)
				return

			for otherCar in self.cars:
				if otherCar == car: continue

				otherCarNextPos = otherCar.getNextPosition()
				otherCarDirection = otherCarNextPos - otherCar.position
				if otherCarNextPos == nextPos:
					car.collide(otherCar, direction)
					otherCar.collide(car, otherCarDirection)
					# TODO: head collision vs side collision

					self.addExplosion(car.position)
					break

	def addExplosion(self, position):
		self.sprites.append(Explosion(position))

	def draw(self, rgb):
		Game.draw(self, rgb)

		self.map.draw(rgb, self.mode == GameMode.Simulate)

		for car in self.cars:
			car.draw(rgb)

		for sprite in self.sprites:
			sprite.draw(rgb)

	def isZero(self, d):
		return abs(d) < 0.1

	def notIsZero(self, d):
		return abs(d) > 0.1

	def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
		Game.onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis)

		if self.mode == GameMode.PlayerInput:
			if player == self.currentPlayer:
				if (self.notIsZero(xAxis) and self.isZero(previousXAxis)) or \
				   (self.notIsZero(yAxis) and self.isZero(previousYAxis)):
					x = 1 if xAxis > 0.1 else 0
					x = -1 if xAxis < -0.1 else x
					y = 1 if yAxis > 0.1 else 0
					y = -1 if yAxis < -0.1 else y

					print x,y,"   ",xAxis,previousXAxis,yAxis, previousYAxis,"==================================="
					self.cars[self.currentPlayer].addMovement(Vector(x, y))

	def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
		Game.onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton)

		if self.mode == GameMode.PlayerInput:
			if player == self.currentPlayer:
				if not aButton and previousAButton:
					self.nextPlayer()

if __name__ == "__main__":
	print "Starting game"
	#sample = BoxCar("127.0.0.1")
	sample = BoxCar("192.168.1.22")
	sample.run()
	print "Stopping game"

