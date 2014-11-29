#!/usr/bin/python
# -*- coding: utf8 -*-
import math
import time
from gamelib import Vector, PIXEL_DIM_X, BLACK, RED
from gamelib.animation import AnimationLoopType
from gamelib.sprite import Sprite

from gamelib.state import State


class FullscreenSprite(Sprite):
    def __init__(self, winner_color):
        sprite1 = [{ 'position': Vector( i % PIXEL_DIM_X, math.floor(i / PIXEL_DIM_X)), 'color': winner_color } for i in range(96)]
        sprite2 = [{ 'position': Vector( i % PIXEL_DIM_X, math.floor(i / PIXEL_DIM_X)), 'color': BLACK } for i in range(96)]

        Sprite.__init__(self, [sprite1, sprite2, sprite1, sprite2, sprite1], 2, AnimationLoopType.OneTime)


class GameOverState(State):
    def __init__(self):
        State.__init__(self, "GameOver")

        self.started = time.time()
        self.sprite = FullscreenSprite(RED)

    def update(self, dt):
        State.update(self, dt)

        if time.time() > self.started + 3000:
            self.ended = True
        else:
            self.sprite.update(dt)

    def draw(self, rgb):
        State.draw(self, rgb)

        self.sprite.draw(rgb)