# -*- coding: utf8 -*- 

"""gameobject.py: Represents an object in a game. """

from vector import *
from librgb import *


class GameObject(object):
    """ The GameObject class represents an object in a game.
    It is mostly used as a base class for
    other elements that enrich it's capabilities.

    If used should be updated and drawn.
    """

    def __init__(self):
        self.position = Vector(0, 0)
        self.width = 1
        self.height = 1
        self.color = WHITE

    def update(self, dt):
        pass

    def draw(self, rgb):
        for x in range(self.width):
            for y in range(self.height):
                rgb.setPixel(self.position + Vector(x, y).toIntArr(), self.color)