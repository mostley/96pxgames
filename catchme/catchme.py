#!/usr/bin/python
# -*- coding: utf8 -*-

import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.game import *
from gamelib.animatedgameobject import AnimatedGameObject
from gamelib.state import State
from gamelib.sprites.explosion import Explosion


class CatchMe(Game):

    def __init__(self, ip):
        Game.__init__(self, ip, [
            Sound('tock', 'sounds/tock.wav')
        ], [], [
            MainState()
        ])

        self.setState("Main")


class MainState(State):

    def __init__(self):
        State.__init__(self, "Main")


        w = PIXEL_DIM_X - 1
        h = PIXEL_DIM_Y - 1

        self.point = Vector(6, 4)

        self.characters = [
            AnimatedGameObject(Vector(0, 0), RED, BLUE),
            AnimatedGameObject(Vector(w, 0), BLUE, RED),
            AnimatedGameObject(Vector(0, h), GREEN, BLUE),
            AnimatedGameObject(Vector(w, h), YELLOW, BLUE)
        ]

        self.explosion = None

        for character in self.characters:
            character.score = 0

    def update(self, dt):
        State.update(self, dt)

        if self.explosion:
            self.explosion.update(dt)

        for character in self.characters:
            character.update(dt)

            if character.position.toInt() == self.point.toInt():
                character.score += 1
                character.animation.duration = 1.0/character.score 

                self.point = Vector.random([PIXEL_DIM_X-1, PIXEL_DIM_Y-1])

                if character.score > 5:
                    character.score = 0
                    character.animation.duration = 1.0

                    self.explosion = Explosion(character.position)


    def draw(self, rgb):
        State.draw(self, rgb)

        for character in self.characters:
            character.draw(rgb)

        if self.explosion:
            self.explosion.draw(rgb)

            if self.explosion.ended:
                self.explosion = None

        if self.point:
            rgb.setPixel(self.point, TURQUE)

    def onAxisChanged(self, player, x, y, px, py):
        State.onAxisChanged(self, player, x, y, px, py)

        self.characters[player].velocity = Vector(x, y)

        self.game.playSound('tock')

if __name__ == "__main__":
    print "Starting game"
    sample = CatchMe("127.0.0.1")
    sample.run()
    print "Stopping game"
