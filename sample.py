#!/usr/bin/python
# -*- coding: utf8 -*-

from gamelib.game import *
from gamelib.animatedgameobject import AnimatedGameObject
from gamelib.state import State


class SampleGame(Game):

    def __init__(self, ip):
        Game.__init__(self, ip, [
            Sound('tock', 'boxcar/sounds/tock1.wav')
        ], [{
            "name": 'main',
            "file": 'boxcar/sounds/music_interesting.ogg'
        }], [
            MainState()
        ])

        self.setState("Main")
        self.music.play('main')


class MainState(State):

    def __init__(self):
        State.__init__(self, "Main")

        w = PIXEL_DIM_X - 1
        h = PIXEL_DIM_Y - 1

        self.characters = [
            AnimatedGameObject(Vector(0, 0), RED),
            AnimatedGameObject(Vector(w, 0), BLUE),
            AnimatedGameObject(Vector(0, h), GREEN),
            AnimatedGameObject(Vector(w, h), YELLOW)
        ]

    def update(self, dt):
        State.update(self, dt)

        for character in self.characters:
            character.update(dt)

    def draw(self, rgb):
        State.draw(self, rgb)

        for character in self.characters:
            character.draw(rgb)

    def onAxisChanged(self, player, x, y, px, py):
        State.onAxisChanged(self, player, x, y, px, py)

        self.characters[player].velocity = Vector(x, y)

        self.game.playSound('tock')

if __name__ == "__main__":
    print "Starting game"
    sample = SampleGame("127.0.0.1")
    sample.run()
    print "Stopping game"
