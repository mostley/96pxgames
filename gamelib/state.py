# -*- coding: utf8 -*- 

class State:
	def __init__(self, name):
		self.name = name

	def update(self, dt):
		pass

	def draw(self, rgb):
		pass

	def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
		pass

	def onClampedAxisChanged(self, player, x, y):
		pass

	def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
		pass

	def onEnter(self, oldState):
		pass

	def onLeave(self, newState):
		pass