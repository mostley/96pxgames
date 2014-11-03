#!/usr/bin/python
# -*- coding: utf8 -*- 

import sys, os, subprocess

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.game import *
from gamelib.menu import *

from gamesimulation import *

class GameState(State):
    def __init__(self):
        State.__init__(self, "game")

        self.ended = False
        self.gamename = None

    def update(self, dt):
        if self.gamename != None:
            subprocess.check_call("python ../" + self.gamename + "/" + self.gamename + ".py", cwd='../' + self.gamename)

            self.ended = True
            self.gamename = None

class GameSelector(Game):

    def __init__(self, ip):

        self.games = []
        excludedFolders = ['simulator', 'selector', 'gamelib', '.git', '.idea']
        for directory in os.listdir('..'):
            if not os.path.isdir(os.path.join('..', directory)):
                continue
            if directory in excludedFolders:
                continue
            print directory
            self.games.append(directory)

        self.startmenu = Menu(self, 'startmenu', self.games)
        self.gamestate = GameState()
        Game.__init__(self, ip, states = [self.startmenu, self.gamestate])

        self.setState('startmenu')

    def update(self, dt):
        Game.update(self, dt)

        if self.gamestate.ended:
            self.setState('startmenu')

        elif self.startmenu.result != None:
            self.gamestate.gamename = self.startmenu.result
            self.setState('game')

    def draw(self, rgb):
        Game.draw(self, rgb)

    def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
        Game.onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis)

    def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
        Game.onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton)

if __name__ == "__main__":
    print "Starting game"
    game = GameSelector("127.0.0.1")
    game.run()
    print "Stopping game"

