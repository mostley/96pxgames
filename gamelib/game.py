#!/usr/bin/python
# -*- coding: utf8 -*- 

from librgb import *
import time
import pygame

class Game:
	def __init__(self, playerCount, ip="192.168.1.5"):
		self.rgb = RGB(ip)
		self.rgb.invertedX = True
		self.rgb.invertedY = True

		self.framerate = 40

		self.previousControllerState = []
		self.controllers = []

		pygame.init()
		pygame.joystick.init()
		for i in range(playerCount):
			joystick = pygame.joystick.Joystick(i)
			self.controllers.append(joystick)
			joystick.init()
			self.previousControllerState.append({
				'xAxis': 0,
				'yAxis': 0,
				'aButton': False,
				'bButton': False
			})

		self.lastFrame = time.time()

	def poll(self, dt):
		pygame.event.pump()

		for player in range(len(self.controllers)):
			controller = self.controllers[player]
			previousControllerState = self.previousControllerState[player]

			xAxis = -controller.get_axis(0)
			yAxis = -controller.get_axis(1)
			previousXAxis = previousControllerState['xAxis']
			previousYAxis = previousControllerState['yAxis']
			xChanged = previousXAxis != xAxis
			yChanged = previousYAxis != yAxis

			if xChanged or yChanged:
				self.onAxisChanged(player, xAxis, yAxis, previousXAxis, previousYAxis)

				previousControllerState['xAxis'] = xAxis
				previousControllerState['yAxis'] = yAxis

			aButton = controller.get_button(0)
			bButton = controller.get_button(1)
			previousAButton = previousControllerState['aButton']
			previousBButton = previousControllerState['bButton']
			aChanged = previousAButton != aButton
			bChanged = previousBButton != bButton

			if aChanged or bChanged:
				self.onButtonChanged(player, aButton, bButton, previousAButton, previousBButton)

				previousControllerState['aButton'] = aButton
				previousControllerState['bButton'] = bButton

	def run(self):
		clock = pygame.time.Clock()
		while True:
			dt = clock.tick(self.framerate) / 1000.0
			#dt = time.time() - self.lastFrame

			self.poll(dt)

			self.update(dt)

			self.draw(self.rgb)

			self.rgb.send()

			self.lastFrame = time.time()

	def update(self, dt):
		pass

	def draw(self, rgb):
		rgb.clear(BLACK)

	def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
		pass

	def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
		pass


