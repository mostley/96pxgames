#!/usr/bin/python
# -*- coding: utf8 -*- 

import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.game import *
from gamelib.menu import *

from gamesimulation import *


class ShooterGame(Game):

	def __init__(self, ip):
		Game.__init__(self, ip)

		self.startmenu = Menu(self, 'startmenu', ['Start', 'SomethingElse'])
		self.currentState = self.startmenu

	def update(self, dt):
		Game.update(self, dt)

		self.currentState.update(dt)

	def draw(self, rgb):
		Game.draw(self, rgb)

		self.currentState.draw(rgb)

	def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
		Game.onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis)

		self.currentState.onAxisChanged(player, xAxis, yAxis, previousXAxis, previousYAxis)

	def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
		Game.onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton)

		self.currentState.onButtonChanged(player, player, aButton, bButton, previousAButton, previousBButton)

if __name__ == "__main__":
	print "Starting game"
	game = ShooterGame("127.0.0.1")
	game.run()
	print "Stopping game"

