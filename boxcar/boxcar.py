#!/usr/bin/python
# -*- coding: utf8 -*- 

import sys, os
from random import shuffle

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.game import *
from gamelib.sound import *

# boxcar files
from car import *
from map import *
from explosion import *
from winsprite import *

class GameMode:
	Bootstrap = 0
	PlayerInput = 1
	Simulate = 2
	GameOver = 3

class Sounds:
	tock1 = 'tock1'
	tock2 = 'tock2'
	explode = 'explode'
	fanfare = 'fanfare'
	fanfare_lost = 'fanfare_lost'

class Music:
	music_slow = 'music_slow'
	music_interesting = 'music_interesting'

class BoxCar(Game):

	def __init__(self, ip):
		Game.__init__(self, ip, [
			Sound(Sounds.tock1, 'sounds/tock1.wav'),
			Sound(Sounds.tock2, 'sounds/tock2.wav'),
			Sound(Sounds.explode, 'sounds/explode.wav'),
			Sound(Sounds.fanfare, 'sounds/fanfare.ogg'),
			Sound(Sounds.fanfare_lost, 'sounds/fanfare_lost.ogg'),
		],[{
			"name": Music.music_slow, 
			"file": 'sounds/music_slow.ogg', 
			"volume": 0.1
		},{
			"name": Music.music_interesting, 
			"file": 'sounds/music_interesting.ogg',
			"volume": 1
		}])

		self.map = Map()
		carColors = [ORANGE, BLUE, TURQUE, YELLOW]

		self.cars = [Car(self.map.spawnpoints[i].clone(), carColors[i]) for i in range(self.playerCount)]

		self.currentPlayer = 0
		self.mode = GameMode.Bootstrap

		self.setMode(GameMode.Bootstrap)

		self.sprites = []

		self.inputOrder = []
		self.setInputOrder()

		self.winner = None
		self.gameOverAnimation = None

		self.simulationPause = 0

		if self.playerCount == 0:
			raise Exception("not enough players")

	def simulationIsOver(self):
		result = True

		for car in self.cars:
			if car.hasMovements():
				result = False
				break

		return result

	def setInputOrder(self):
		self.inputOrder = [i for i in range(self.playerCount) if not self.cars[i].isDead]
		#shuffle(self.inputOrder)

	def setMode(self, mode):
		if self.mode != mode:
			self.mode = mode

			if self.mode == GameMode.PlayerInput:
				self.setInputOrder()
				print "PlayerInput Mode"
				
				for car in self.cars:
					car.setInputMode(True)
				
				self.music.play(Music.music_slow)
			elif self.mode == GameMode.Simulate:
				self.setInputOrder()
				print "Simulation Mode"
				
				for car in self.cars:
					car.setInputMode(False)

				self.music.play(Music.music_interesting)
			elif self.mode == GameMode.Bootstrap:
				print "Bootstrap Mode"
			elif self.mode == GameMode.GameOver:
				print "GameOver Mode"
				if self.winner != None:
					self.playSound(Sounds.fanfare)
				else:
					self.playSound(Sounds.fanfare_lost)
				self.music.pause()
			else:
				print "Unknown Mode"

	def nextPlayer(self):
		if len(self.inputOrder) > 0:
			self.currentPlayer = self.inputOrder.pop()
			while len(self.inputOrder) > 0 and self.cars[self.currentPlayer].isDead:
				self.currentPlayer = self.inputOrder.pop()

		if len(self.inputOrder) <= 0:
			self.setMode(GameMode.Simulate)

	def update(self, dt):
		if self.mode == GameMode.GameOver:
			self.gameOverAnimation.update(dt)
			if self.gameOverAnimation.ended:
				self.restart()
		elif self.mode == GameMode.Simulate:
			if self.simulationIsOver():
				self.setMode(GameMode.PlayerInput)
		elif self.mode == GameMode.PlayerInput:
			Game.update(self, dt)
			if self.cars[self.currentPlayer].isDead:
				self.nextPlayer()

			lastCars = [car for car in self.cars if not car.isDead]
			if len(lastCars) <= 1:
				self.winner = None if len(lastCars) <= 0 else lastCars[0]
				winnercolor = (0,0,0)
				if self.winner != None:
					winnercolor =self.winner.color
				self.gameOverAnimation = WinSprite(winnercolor)
				self.setMode(GameMode.GameOver)
		elif self.mode == GameMode.Bootstrap:
			self.setMode(GameMode.PlayerInput)
		else:
			print "unknown Game mode"
		
		self.map.update(dt)

		if self.simulationPause <= 0:
			for player in range(len(self.cars)):
				car = self.cars[player]
				if car.isDead:
					car.isActive = False
				else:
					car.isActive = self.mode == GameMode.Simulate
					car.isHightlighted = self.mode == GameMode.PlayerInput and self.currentPlayer == player

					self.collisionHandling(car)
					car.update(dt)

		self.sprites = [sprite for sprite in self.sprites if not sprite.ended]
		for sprite in self.sprites:
			sprite.update(dt)

		self.simulationPause -= dt

	def collisionHandling(self, car):
		if car.isActive and car.hasMovements():
			nextPos = car.getNextPosition()
			if nextPos:
				direction = nextPos - car.position

				block = self.map.getBlockAt(nextPos)
				if block != None:
					car.collide(block, direction)
					self.addExplosion(car.position)
					return

				for otherCar in self.cars:
					if otherCar == car: continue

					otherCarNextPos = otherCar.getNextPosition()
					otherCarNextPos = otherCar.position if not otherCarNextPos else otherCarNextPos
					otherCarDirection = otherCarNextPos - otherCar.position
					if otherCarNextPos == nextPos:
						car.collide(otherCar, direction)
						otherCar.collide(car, otherCarDirection)
						
						self.addExplosion(car.position)
						break

					for trailDot in otherCar.trail:
						if trailDot == nextPos:
							car.collide(otherCar, direction)
							
							self.addExplosion(car.position)


	def addExplosion(self, position):
		explosion = Explosion(position)
		self.sprites.append(explosion)
		self.playSound(Sounds.explode)

		self.simulationPause = explosion.duration

	def draw(self, rgb):
		Game.draw(self, rgb)

		self.map.draw(rgb, self.mode == GameMode.Simulate)

		for car in self.cars:
			if not car.isDead:
				car.draw(rgb)

		for sprite in self.sprites:
			sprite.draw(rgb)

		if self.gameOverAnimation:
			self.gameOverAnimation.draw(rgb)

	def restart(self):
		print "Restart Game"
		for car in self.cars:
			car.reset()

		self.setInputOrder()

		for i in range(self.playerCount):
			self.cars[i].position = self.map.spawnpoints[i].clone()

		self.setMode(GameMode.PlayerInput)

	def isZero(self, d):
		return abs(d) < 0.1

	def notIsZero(self, d):
		return abs(d) > 0.1

	def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
		Game.onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis)

		if self.mode == GameMode.PlayerInput:
			if player == self.currentPlayer:
				if (self.notIsZero(xAxis) and self.isZero(previousXAxis)) or \
				   (self.notIsZero(yAxis) and self.isZero(previousYAxis)):

					self.playSound(Sounds.tock1 if abs(xAxis) > 0.1 else Sounds.tock2)

					x = 1 if xAxis > 0.1 else 0
					x = -1 if xAxis < -0.1 else x
					y = 1 if yAxis > 0.1 else 0
					y = -1 if yAxis < -0.1 else y

					self.cars[self.currentPlayer].addMovement(Vector(x, y))

	def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
		Game.onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton)

		if self.mode == GameMode.PlayerInput:
			if player == self.currentPlayer:
				if not aButton and previousAButton:
					self.nextPlayer()

if __name__ == "__main__":
	print "Starting game"
	sample = BoxCar("127.0.0.1")
	#sample = BoxCar("192.168.1.22")
	sample.run()
	print "Stopping game"

