#!/usr/bin/python
# -*- coding: utf8 -*- 

import sys, os
from random import shuffle, choice

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.game import *
from gamelib.sound import *
from gamelib.animation import *
from car import *
from map import *
from explosion import *
from winsprite import *

class GameMode:
    Bootstrap = 0
    PlayerInput = 1
    Simulate = 2
    GameOver = 3
    LevelSelect = 4

class Sounds:
    tock1 = 'tock1'
    tock2 = 'tock2'
    explode = 'explode'
    fanfare = 'fanfare'
    fanfare_lost = 'fanfare_lost'
    freeze = 'freeze'
    unfreeze = 'unfreeze'
    fatz = 'fatz'

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
            Sound(Sounds.freeze, 'sounds/freeze.wav'),
            Sound(Sounds.unfreeze, 'sounds/unfreeze.wav'),
            Sound(Sounds.fatz, 'sounds/fatz.wav'),
        ],[{
            "name": Music.music_slow,
            "file": 'sounds/music_slow.ogg',
            "volume": 0.1
        },{
            "name": Music.music_interesting,
            "file": 'sounds/music_interesting.ogg',
            "volume": 1
        }])


        self.maps = [
            Map(f) for f in [
                'maps/default.blocks',
                'maps/empty.blocks',
                'maps/minimal.blocks',
                'maps/box.blocks'
            ]
        ]
        self.mapIsSelected = False
        self.mapSelectorPlayer = choice(range(self.playerCount))
        self.map = self.maps[0]
        self.currentMapIndex = 0
        self.blinkAnimation = Animation(0, 1, 0.25, AnimationLoopType.PingPong)

        self.carColors = [ORANGE, BLUE, TURQUE, YELLOW]

        self.cars = []
        self.spawnCars()

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

    def spawnCars(self):
        self.cars = [Car(self.map.spawnpoints[i].position.clone(), self.carColors[i]) for i in range(self.playerCount)]

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

                self.playSound(Sounds.freeze)
                self.music.play(Music.music_slow)
            elif self.mode == GameMode.Simulate:
                self.setInputOrder()
                print "Simulation Mode"

                for car in self.cars:
                    car.setInputMode(False)

                self.playSound(Sounds.unfreeze)
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
            elif self.mode == GameMode.LevelSelect:
                print "Level Selection Mode"

                self.music.play(Music.music_slow)
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
            self.setMode(GameMode.LevelSelect)
        elif self.mode == GameMode.LevelSelect:
            Game.update(self, dt)
            self.blinkAnimation.update(dt)

            if self.mapIsSelected:
                self.setMode(GameMode.PlayerInput)
        else:
            print "unknown Game mode"

        self.updateMap(dt)

    def updateMap(self, dt):
        if self.map == None: return
        if not self.mapIsSelected: return

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

        self.drawMap(rgb)

    def drawMap(self, rgb):
        if self.map == None: return
        if self.mode == GameMode.LevelSelect:
            if self.blinkAnimation.currentValue > 0.5:
                return

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

        self.setInputOrder()

        self.spawnCars()

        self.setMode(GameMode.LevelSelect)
        self.mapIsSelected = False
        self.mapSelectorPlayer += 1
        if self.mapSelectorPlayer >= self.playerCount:
            self.mapSelectorPlayer = 0

    def selectCurrentMap(self):
        self.mapIsSelected = True

    def nextMap(self):
        self.currentMapIndex += 1
        if self.currentMapIndex >= len(self.maps):
            self.currentMapIndex = 0

        self.map = self.maps[self.currentMapIndex]
        self.spawnCars()

    def previousMap(self):
        self.currentMapIndex -= 1
        if self.currentMapIndex < 0:
            self.currentMapIndex = len(self.maps) - 1

        self.map = self.maps[self.currentMapIndex]
        self.spawnCars()

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
        elif self.mode == GameMode.LevelSelect:
            if player == 0:
                if self.notIsZero(xAxis) and self.isZero(previousXAxis):
                    if xAxis > 0.1:
                        self.nextMap()
                    elif xAxis < -0.1:
                        self.previousMap()

    def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
        Game.onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton)

        if self.mode == GameMode.PlayerInput:
            if player == self.currentPlayer:
                if not aButton and previousAButton:
                    self.nextPlayer()
        elif self.mode == GameMode.LevelSelect:
            if player == 0:
                if not aButton and previousAButton:
                    self.selectCurrentMap()

if __name__ == "__main__":
    print "Starting game"
    ip = "127.0.0.1"
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    sample = BoxCar(ip)
    sample.run()
    print "Stopping game"

