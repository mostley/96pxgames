# -*- coding: utf8 -*- 

from state import *

class StateMachine:
	def __init__(self, states):
		self.states = {}
		for state in states:
			self.states[state.name] = state

		self.currentState = None

	def setState(self, name):
		if not self.states.has_key(name):
			raise Exception("state '" + name + "' does not exist")

		newState = self.states[name]
		oldState = self.currentState

		if self.currentState:
			self.currentState.onLeave(newState)

		self.currentState = newState
		self.currentState.onEnter(oldState)

	def update(self, dt):
		if self.currentState:
			self.currentState.update(dt)

	def draw(self, rgb):
		if self.currentState:
			self.currentState.draw(rgb)

	def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
		if self.currentState:
			self.currentState.onAxisChanged(player, xAxis, yAxis, previousXAxis, previousYAxis)

	def onClampedAxisChanged(self, player, x, y):
		if self.currentState:
			self.currentState.onClampedAxisChanged(player, x, y)

	def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
		if self.currentState:
			self.currentState.onButtonChanged(player, aButton, bButton, previousAButton, previousBButton)