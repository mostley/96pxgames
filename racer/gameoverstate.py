#!/usr/bin/python
# -*- coding: utf8 -*-

from gamelib.state import State


class GameOverState(State):
    def __init__(self):
        State.__init__(self, "GameOver")

    def update(self, dt):
        State.update(self, dt)

    def draw(self, rgb):
        State.draw(self, rgb)