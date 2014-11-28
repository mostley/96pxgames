#!/usr/bin/python
# -*- coding: utf8 -*-

from gamelib.vector import *
from gamelib.color import *
from gamelib.animatedgameobject import AnimatedGameObject


class Ship(AnimatedGameObject):
    def __init__(self, position, color1, color2):
        AnimatedGameObject.__init__(self, position, color1, color2)

        self.speed = 5
        self.friction = 1.0

    def update(self, dt):
        self.animation.update(dt)
        self.color = self.animation.getValue()

    def draw(self, rgb):

        rgb.setPixel(self.position, self.color)
        rgb.mix_color(self.position + Vector(0, -1).toIntArr(), YELLOW, 1)
        rgb.mix_color(self.position + Vector(-1, -1).toIntArr(), YELLOW, 0.1)
        rgb.mix_color(self.position + Vector(1, -1).toIntArr(), YELLOW, 0.1)