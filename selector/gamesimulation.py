# -*- coding: utf8 -*- 

from gamelib.state import *

class GameSimulation(State):
	def __init__(self, game):
		State.__init__(self, "game")

		self.game = game

		self.characters = [
			AnimatedGameObject(Vector(0,0), RED, BLUE, 1, AnimationAlgorithm.Linear), 
			AnimatedGameObject(Vector(PIXEL_DIM_X-1, 0), BLUE, GREEN, 1, AnimationAlgorithm.EaseInQuad), 
			AnimatedGameObject(Vector(PIXEL_DIM_X-1, PIXEL_DIM_Y-1), GREEN, YELLOW, 1, AnimationAlgorithm.EaseOutQuad), 
			AnimatedGameObject(Vector(0, PIXEL_DIM_Y-1), YELLOW, BLUE, 1, AnimationAlgorithm.EaseInOutQuad)
		]

		self.blocks = []

	def update(self, dt):
		State.update(self, dt)
		
		for i in range(self.playerCount):
			self.characters[i].update(dt)
		
		for block in self.blocks:
			block.update(dt)

	def draw(self, rgb):
		State.update(self, rgb)

		for i in range(self.playerCount):
			self.characters[i].draw(rgb)
		
		for block in self.blocks:
			block.draw(rgb)

	def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
		State.update(self, player, xAxis, yAxis, previousXAxis, previousYAxis)

		if xAxis != previousXAxis or yAxis != previousYAxis:
			self.characters[player].velocity += Vector(xAxis, yAxis)

	def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
		State.update(self, player, aButton, bButton, previousAButton, previousBButton)