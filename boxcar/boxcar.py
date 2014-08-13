#!/usr/bin/python
# -*- coding: utf8 -*- 

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.game import *
from car import *
from map import *

class GameMode:
	Bootstrap = 0
	PlayerInput = 1
	Simulate = 2

class BoxCar(Game):

	def __init__(self, ip):
		Game.__init__(self, ip)

		self.map = Map()
		carColors = [RED, BLUE, GREEN, YELLOW]

		self.cars = [Car(self.map.spawnpoints[i], carColors[i]) for i in range(self.playerCount)]

		self.currentPlayer = 0
		self.mode = GameMode.Bootstrap

		self.setMode(GameMode.Bootstrap)

	def simulationIsOver(self):
		result = True

		for player in range(self.playerCount):
			if self.cars[player].hasMovements():
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

		for player in range(self.playerCount):
			self.cars[player].update(dt)
			self.cars[player].isActive = self.mode == GameMode.Simulate
			self.cars[player].isHightlighted = self.mode == GameMode.PlayerInput and self.currentPlayer == player
		
		self.map.update(dt)

	def draw(self, rgb):
		Game.draw(self, rgb)

		self.map.draw(rgb, self.mode == GameMode.Simulate)

		for player in range(self.playerCount):
			self.cars[player].draw(rgb)

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
	sample = BoxCar("127.0.0.1")
	sample.run()
	print "Stopping game"

