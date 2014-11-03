#!/usr/bin/python
# -*- coding: utf8 -*- 

import sys, os
from random import shuffle
from diamondsquare import DiamondSquare

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.game import *
from gamelib.color import *
from gamelib.sound import *


class TowerDefense(Game):

    def __init__(self, ip):
        Game.__init__(self, ip, [], [])

        self.map = DiamondSquare(12, 8).create()
        self.delta = 0

    def update(self, dt):
        Game.update(self, dt)

        if self.delta > 2:
            print "update"
            self.map = DiamondSquare(12, 8).create()
            self.delta = 0
        self.delta += dt

    def draw(self, rgb):
        Game.draw(self, rgb)

        for x in range(int(self.map.w)):
            for y in range(int(self.map.h)):
                #print x,y,self.map.w,self.map.h
                v = self.map.data[int(x)][int(y)]
                if not v:
                    v = 0

                rgb.setPixel(Vector(x, y), self.get_color_by_height(v))

    def get_color_by_height(self, height):
        result = (0,0,0)
        height *= 5

        if height < 30:
            height -= 10
            height /= 20
            result = Color.multiply((0, 100, 100), height)
        elif height < 50:
            height -= 30
            height /= 20
            result = Color.multiply((80, 45, 15), height)
        elif height < 80:
            height -= 50
            height /= 30
            result = Color.multiply((0, 255, 0), height)
        elif height < 100:
            #height -= 80
            result = (height, height, height)
        elif height < 200:
            #height -= 100
            result = (height,height,height)
        else:
            result = (255,255,255)

        return result

    def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
        Game.onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis)

    def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
        Game.onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton)


if __name__ == "__main__":
    print "Starting game"
    ip = "127.0.0.1"
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    game = TowerDefense(ip)
    game.run()
    print "Stopping game"

