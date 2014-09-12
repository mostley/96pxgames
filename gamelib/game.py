#!/usr/bin/python
# -*- coding: utf8 -*- 

from librgb import *
import time, StringIO, pygame, sys, os
from keyboardcontroller import KeyboardController

class Game:
	def __init__(self, ip="192.168.1.5"):
		self.rgb = RGB(ip)
		self.rgb.invertedX = False
		self.rgb.invertedY = True

		self.framerate = 20

		self.previousControllerState = []
		self.controllers = []

		pygame.init()
		pygame.joystick.init()
		pygame.display.set_mode([200,100])
		self.playerCount = pygame.joystick.get_count()
		print str(self.playerCount) + " Joysticks connected."

		for i in range(self.playerCount):
			joystick = pygame.joystick.Joystick(i)
			self.controllers.append(joystick)
			joystick.init()
			self.previousControllerState.append({
				'xAxis': 0,
				'yAxis': 0,
				'aButton': False,
				'bButton': False
			})
		
		self.keyboardJoystick = False
		if self.playerCount == 0:
			self.playerCount = 2
			self.keyboardJoystick = True
			self.previousControllerState.append({
				'xAxis': 0,
				'yAxis': 0,
				'aButton': False,
				'bButton': False
			})
			self.controllers.append(KeyboardController(id=0))
			self.previousControllerState.append({
				'xAxis': 0,
				'yAxis': 0,
				'aButton': False,
				'bButton': False
			})
			self.controllers.append(KeyboardController(id=1))

		self.lastFrame = time.time()

	def poll(self, dt):
		pygame.event.pump()
		
		
		if self.keyboardJoystick:
			events = pygame.event.get()
		
		for player in range(len(self.controllers)):
			controller = self.controllers[player]
			
			if self.keyboardJoystick:
				controller.set_events(events)
			
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

			self.update(dt)

			self.draw(self.rgb)

			self.rgb.send()

			self.lastFrame = time.time()

	def update(self, dt):
		self.poll(dt)

	def draw(self, rgb):
		rgb.clear(BLACK)

	def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
		pass

	def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
		pass


