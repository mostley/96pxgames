#!/usr/bin/python
# -*- coding: utf8 -*- 

from librgb import *
import time, StringIO, pygame, sys, os
from sound import Sound
from music import MusicManager
from keyboardcontroller import KeyboardController
from statemachine import StateMachine

class Orientation:
    South = 0
    West = 1
    North = 2
    East = 3

    Count = 4

class Game:
    def __init__(self, ip="127.0.0.1", resources=None, songs=None, states=None):
        self.rgb = RGB(ip)
        self.rgb.invertedX = False
        self.rgb.invertedY = True

        self.framerate = 20

        self.previousControllerState = []
        self.controllers = []
        self.controllerOrientations = []

        if not resources:
            resources = []
        if not songs:
            songs = []
        if not states:
            states = []

        self.stateMachine = StateMachine(states)

        self.music = MusicManager(songs)

        pygame.init()
        pygame.joystick.init()
        pygame.mixer.init()

        self.resources = {}
        for r in resources:
            r.load()
            if self.resources.has_key(r.name):
                print "double resource key: '", r.name,"'"

            self.resources[r.name] = r

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
                'bButton': False,
                'cButton': False,
                'dButton': False
            })
            self.controllerOrientations.append(Orientation.South)

        self.keyboardJoystick = False
        if self.playerCount == 0:
            self.playerCount = 2
            self.keyboardJoystick = True
            self.previousControllerState.append({
                'xAxis': 0,
                'yAxis': 0,
                'aButton': False,
                'bButton': False,
                'cButton': False,
                'dButton': False
            })
            self.controllers.append(KeyboardController(id=0))
            self.controllerOrientations.append(Orientation.South)

            self.previousControllerState.append({
                'xAxis': 0,
                'yAxis': 0,
                'aButton': False,
                'bButton': False,
                'cButton': False,
                'dButton': False
            })
            self.controllers.append(KeyboardController(id=1))
            self.controllerOrientations.append(Orientation.South)

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
                xAxis, yAxis = self._mapAxisToOrientation(player, xAxis, yAxis)
                self.onAxisChanged(player, xAxis, yAxis, previousXAxis, previousYAxis)

                previousControllerState['xAxis'] = xAxis
                previousControllerState['yAxis'] = yAxis

            aButton = controller.get_button(0)
            bButton = controller.get_button(1)
            cButton = controller.get_button(2)
            dButton = controller.get_button(3)
            previousAButton = previousControllerState['aButton']
            previousBButton = previousControllerState['bButton']
            previousCButton = previousControllerState['cButton']
            previousDButton = previousControllerState['dButton']
            aChanged = previousAButton != aButton
            bChanged = previousBButton != bButton
            cChanged = previousCButton != cButton
            dChanged = previousDButton != dButton

            if aChanged or bChanged:
                self.onButtonChanged(player, aButton, bButton, previousAButton, previousBButton)

                previousControllerState['aButton'] = aButton
                previousControllerState['bButton'] = bButton

            if cChanged:
                if not cButton:
                    self._onChangeOrientation(player)

                previousControllerState['cButton'] = cButton

            if dChanged:
                if not dButton:
                    self.onStartMenuTriggered(player)

                previousControllerState['dButton'] = dButton

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

        self.stateMachine.update(dt)

    def draw(self, rgb):
        rgb.clear(BLACK)

        self.stateMachine.draw(rgb)

    def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
        #todo rotation

        if (self._notIsZero(xAxis) and self._isZero(previousXAxis)) or \
           (self._notIsZero(yAxis) and self._isZero(previousYAxis)):

            x = 1 if xAxis > 0.1 else 0
            x = -1 if xAxis < -0.1 else x
            y = 1 if yAxis > 0.1 else 0
            y = -1 if yAxis < -0.1 else y

            if x != 0 or y != 0:
                self.onClampedAxisChanged(player, x, y)

        self.stateMachine.onAxisChanged(player, xAxis, yAxis, previousXAxis, previousYAxis)

    def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
        self.stateMachine.onButtonChanged(player, aButton, bButton, previousAButton, previousBButton)

    def onClampedAxisChanged(self, player, x, y):
        self.stateMachine.onClampedAxisChanged(player, x, y)

    def playSound(self, name):
        res = self.resources[name]
        if isinstance(res, Sound):
            self.resources[name].play()
        else:
            print "tried to play non-sound resource"

    def stopSound(self, name):
        res = self.resources[name]
        if isinstance(res, Sound):
            self.resources[name].stop()
        else:
            print "tried to stop non-sound resource"

    def fadeoutSound(self, name, time):
        res = self.resources[name]
        if isinstance(res, Sound):
            self.resources[name].fadeout(time)
        else:
            print "tried to fadeout non-sound resource"

    def setState(self, name):
        self.stateMachine.setState(name)

    def onStartMenuTriggered(self, player):
        sys.exit(0)

    def _isZero(self, d):
        return abs(d) < 0.1

    def _notIsZero(self, d):
        return abs(d) > 0.1

    def _mapAxisToOrientation(self, player, xAxis, yAxis):
        orientation = self.controllerOrientations[player]

        if orientation == Orientation.North:
            xAxis = -xAxis
            yAxis = -yAxis
        elif orientation == Orientation.West:
            xTmp = xAxis
            xAxis = -yAxis
            yAxis = xTmp
        elif orientation == Orientation.East:
            xTmp = xAxis
            xAxis = yAxis
            yAxis = -xTmp

        return xAxis, yAxis

    def _onChangeOrientation(self, player):
        self.controllerOrientations[player] = (self.controllerOrientations[player] + 1) % Orientation.Count

