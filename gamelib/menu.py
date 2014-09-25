# -*- coding: utf8 -*- 

from gamelib.state import *
from gamelib.animatedgameobject import *
from menuitem import *

class MenuItem(AnimatedGameObject):
	def __init__(self, index, itemType):
		AnimatedGameObject.__init__(self, Vector(index + 1, 1), RED, BLUE, 0, AnimationAlgorithm.Linear)
		self.type = itemType
		self.height = 4
		self.selected = False

	def draw(self, rgb):
		if self.selected:
			self.animation.duration = 1
		else:
			self.animation.duration = 0

		AnimatedGameObject.draw(self, rgb)

class Menu(State):
	def __init__(self, game, name, items):
		State.__init__(self, name)

		self.game = game

		self.menuItems = {}
		for i in range(len(items)):
			name = items[i]
			self.menuItems[name] = MenuItem(i, name)

		self.selectedIndex = 0

	def onItemClicked(self, index):
		pass

	def onEnter(self, oldState):
		State.onEnter(self, oldState)
		self.selectedIndex = 0

	def onLeave(self, newState):
		State.onLeave(self, newState)

	def update(self, dt):
		State.update(self, dt)

		for item in self.menuItems.values():
			item.update(dt)

	def draw(self, rgb):
		State.draw(self, rgb)

		for item in self.menuItems.values():
			item.draw(rgb)

	def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
		State.onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis)

	def onClampedAxisChanged(self, player, x, y):
		State.onClampedAxisChanged(self, player, x, y)

		self.menuItems.values()[self.selectedIndex].selected = False

		self.selectedIndex += x
		if self.selectedIndex >= len(self.menuItems): self.selectedIndex = 0
		if self.selectedIndex < 0: self.selectedIndex = len(self.menuItems)-1
		
		self.menuItems.values()[self.selectedIndex].selected = True

	def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
		State.onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton)

		if not aButton and previousAButton:
			keys = self.menuItems.keys()
			self.onItemClicked(keys[self.selectedIndex])

