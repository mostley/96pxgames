# -*- coding: utf8 -*- 

import math
from gamelib.state import *
from gamelib.animatedgameobject import *

class MenuItem(AnimatedGameObject):
	def __init__(self, index, name, position, size):
		AnimatedGameObject.__init__(self, position, RED, BLUE, 1, AnimationLoopType.PingPong)
		self.name = name
		self.width = size[0]
		self.height = size[1]
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

		self.menuItems = []
		itemCount = len(items)
		for i in range(itemCount):
			name = items[i]
			pos, size = self.layoutMenuItem(i, name, itemCount)
			self.menuItems.append(MenuItem(i, name, pos, size))

		self.selectedIndex = 0

		self.result = None
		self.menuItems[self.selectedIndex].selected = True

	def layoutMenuItem(self, index, name, itemCount):
		if itemCount < 6:
			width = int(math.floor(6/itemCount))
			size = (width, 6)

			pos = Vector(index * (width+1) + 1, 1)
		elif itemCount < 11:
			size = (1, 2)

			y = 5 if index < 5 else 2
			pos = Vector((index % 5) * 2 + 1, y)
		else:
			size = (1, 1)

			y = 6 - (index/5)*2
			pos = Vector((index % 5) * 2 + 1, y)

		return pos, size


	def onItemClicked(self, name):
		self.result = name

	def onEnter(self, oldState):
		State.onEnter(self, oldState)
		self.selectedIndex = 0

	def onLeave(self, newState):
		State.onLeave(self, newState)

	def update(self, dt):
		State.update(self, dt)

		for item in self.menuItems:
			item.update(dt)

	def draw(self, rgb):
		State.draw(self, rgb)

		for item in self.menuItems:
			item.draw(rgb)

	def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
		State.onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis)

	def onClampedAxisChanged(self, player, x, y):

		State.onClampedAxisChanged(self, player, x, y)

		self.menuItems[self.selectedIndex].selected = False

		self.selectedIndex += x
		if self.selectedIndex >= len(self.menuItems): self.selectedIndex = 0
		if self.selectedIndex < 0: self.selectedIndex = len(self.menuItems)-1
		
		self.menuItems[self.selectedIndex].selected = True

	def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
		State.onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton)

		print aButton, previousAButton
		if not aButton and previousAButton:
			item = self.menuItems[self.selectedIndex]
			self.onItemClicked(item.name)

