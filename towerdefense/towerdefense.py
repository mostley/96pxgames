#!/usr/bin/python
# -*- coding: utf8 -*- 

import sys, os
from random import shuffle

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.game import *
from gamelib.sound import *


class TowerDefense(Game):

	def __init__(self, ip):
		Game.__init__(self, ip, [],[])

	def update(self, dt):
		Game.update(dt)

	def draw(self, rgb):
		Game.draw(self, rgb)

	def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
		Game.onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis)


	def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
		Game.onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton)


if __name__ == "__main__":
	print "Starting game"
	game = TowerDefense("127.0.0.1")
	#game = TowerDefense("192.168.1.22")
	game.run()
	print "Stopping game"

