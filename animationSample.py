#!/usr/bin/python
# -*- coding: utf8 -*- 

from gamelib.game import *
from gamelib.animatedgameobject import *

class SampleGame(Game):

    def __init__(self, ip):
        Game.__init__(self, ip)

        self.characters = [
            AnimatedGameObject(Vector(0,0), RED, BLUE, 1, AnimationAlgorithm.Linear), 
            AnimatedGameObject(Vector(PIXEL_DIM_X-1, 0), BLUE, GREEN, 1, AnimationAlgorithm.EaseInQuad), 
            AnimatedGameObject(Vector(PIXEL_DIM_X-1, PIXEL_DIM_Y-1), GREEN, YELLOW, 1, AnimationAlgorithm.EaseOutQuad), 
            AnimatedGameObject(Vector(0, PIXEL_DIM_Y-1), YELLOW, BLUE, 1, AnimationAlgorithm.EaseInOutQuad)
        ]

        self.blocks = [
            AnimatedGameObject(Vector(1,PIXEL_DIM_Y-2), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.Linear),
            AnimatedGameObject(Vector(3,PIXEL_DIM_Y-2), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.EaseInQuad),
            AnimatedGameObject(Vector(5,PIXEL_DIM_Y-2), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.EaseOutQuad),
            AnimatedGameObject(Vector(7,PIXEL_DIM_Y-2), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.EaseInOutQuad),
            AnimatedGameObject(Vector(9,PIXEL_DIM_Y-2), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.EaseInCubic),
            #AnimatedGameObject(Vector(1,PIXEL_DIM_Y-4), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.EaseOutCubic),
            AnimatedGameObject(Vector(3,PIXEL_DIM_Y-4), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.EaseInOutCubic),
            AnimatedGameObject(Vector(5,PIXEL_DIM_Y-4), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.EaseInQuart),
            AnimatedGameObject(Vector(7,PIXEL_DIM_Y-4), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.EaseOutQuart),
            AnimatedGameObject(Vector(9,PIXEL_DIM_Y-4), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.EaseInOutQuart),
            AnimatedGameObject(Vector(1,PIXEL_DIM_Y-6), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.EaseInQuint),
            #AnimatedGameObject(Vector(3,PIXEL_DIM_Y-6), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.EaseOutQuint),
            AnimatedGameObject(Vector(5,PIXEL_DIM_Y-6), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.EaseInOutQuint),
            AnimatedGameObject(Vector(7,PIXEL_DIM_Y-6), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.EaseOutElastic),
            AnimatedGameObject(Vector(9,PIXEL_DIM_Y-6), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.EaseInElastic),
            AnimatedGameObject(Vector(1,PIXEL_DIM_Y-7), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.EaseOutBounce),
            AnimatedGameObject(Vector(3,PIXEL_DIM_Y-7), BLUE, GREEN, 1, AnimationLoopType.PingPong, AnimationAlgorithm.EaseInBounce),
        ]

    def update(self, dt):
        Game.update(self, dt)

        for i in range(self.playerCount):
            self.characters[i].update(dt)

        for block in self.blocks:
            block.update(dt)

    def draw(self, rgb):
        Game.draw(self, rgb)

        for i in range(self.playerCount):
            self.characters[i].draw(rgb)

        for block in self.blocks:
            block.draw(rgb)

    def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
        Game.onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis)

        if xAxis != previousXAxis or yAxis != previousYAxis:
            self.characters[player].velocity += Vector(xAxis, yAxis)

    def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
        Game.onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton)

        print "onButtonChanged"

if __name__ == "__main__":
    print "Starting game"
    sample = SampleGame("127.0.0.1")
    sample.run()
    print "Stopping game"
