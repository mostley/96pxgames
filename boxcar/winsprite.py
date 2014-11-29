# -*- coding: utf8 -*- 

import sys, os, math
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.sprite import *
from gamelib.vector import *
from gamelib.animation import *


class WinSprite(Sprite):
    def __init__(self, winner_color):
        sprite1 = [{ 'position': Vector( i % PIXEL_DIM_X, math.floor(i / PIXEL_DIM_X)), 'color': winner_color } for i in range(96)]
        sprite2 = [{ 'position': Vector( i % PIXEL_DIM_X, math.floor(i / PIXEL_DIM_X)), 'color': BLACK } for i in range(96)]

        Sprite.__init__(self, [sprite1, sprite2, sprite1, sprite2, sprite1], 2, AnimationLoopType.OneTime)
