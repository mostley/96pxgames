# -*- coding: utf8 -*- 

from vector import *
from librgb import *
from gameobject import *
from animation import *


class AnimatedGameObject(GameObject):
    """ The AnimatedGameObject is able to let a pixel animate between two colors. """

    def __init__(self, position, color1, color2, animationDuration=1, loop=AnimationLoopType.Loop, algorithm=AnimationAlgorithm.Linear):
        GameObject.__init__(self)
        self.position = position
        self.color1 = self.color = color1
        self.color2 = color2
        self.animation = Animation(color1, color2, animationDuration, loop, algorithm)
        self.velocity = Vector(0, 0)
        self.speed = 20
        self.friction = 0.7

    def update(self, dt):
        GameObject.update(self, dt)

        self.animation.update(dt)
        self.color = self.animation.getValue()

        self.position += ( self.velocity * dt ) * self.speed
        self.position = self.position.modulo(Vector(PIXEL_DIM_X, PIXEL_DIM_Y))

        self.velocity *= self.friction

    def draw(self, rgb):
        for x in range(self.width):
            for y in range(self.height):
                rgb.setPixel(self.position + Vector(x, y).toIntArr(), self.color)