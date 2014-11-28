#!/usr/bin/python
# -*- coding: utf8 -*-

from gamelib.game import *
from gamelib.sprites.explosion import *

from gamestate import GameState
from gameoverstate import GameOverState


class Racer(Game):

    def __init__(self, ip):
        Game.__init__(self, ip, [], [], [
            GameState(),
            GameOverState()
        ])

        self.setState("Game")

    def update(self, dt):
        Game.update(self, dt)

    def draw(self, rgb):
        Game.draw(self, rgb)

    def onClampedAxisChanged(self, player, x, y):
        Game.onClampedAxisChanged(self, player, x, y)

    def onButtonChanged(self, player, a_button, b_button, previous_a_button, previous_b_button):
        Game.onButtonChanged(self, player, a_button, b_button, previous_a_button, previous_b_button)


if __name__ == "__main__":
    print "Starting game"
    ip = "127.0.0.1"
    #ip = "192.168.0.19"
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    game = Racer(ip)
    game.run()
    print "Stopping game"

