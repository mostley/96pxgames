#!/usr/bin/python
# -*- coding: utf8 -*- 

from gamelib.game import *

class SampleGame(Game):

	def __init__(self, ip):
		Game.__init__(self, ip)

		self.characterPositions = [
			Vector(0,0), 
			Vector(PIXEL_DIM_X-1, 0),
			Vector(PIXEL_DIM_X-1, PIXEL_DIM_Y-1),
			Vector(0, PIXEL_DIM_Y-1)
		]

		self.characterColors = [RED, BLUE, GREEN, YELLOW]

		self.axisVectors = [Vector(0,0),Vector(0,0),Vector(0,0),Vector(0,0)]

		self.characterSpeed = 18

	def update(self, dt):
		Game.update(self, dt)
		
		for player in range(self.playerCount):
			playerPos = self.characterPositions[player] + ( self.axisVectors[player] * dt ) * self.characterSpeed
			self.characterPositions[player] = Vector(playerPos.x % PIXEL_DIM_X, playerPos.y % PIXEL_DIM_Y)

	def draw(self, rgb):
		Game.draw(self, rgb)

		for i in range(self.playerCount):
			rgb.setPixel(self.characterPositions[i], self.characterColors[i])

	def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
		Game.onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis)

		self.axisVectors[player] = Vector(xAxis, yAxis)

	def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
		Game.onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton)

		print "onButtonChanged"

if __name__ == "__main__":
	print "Starting game"
	sample = SampleGame("127.0.0.1")
	sample.run()
	print "Stopping game"

