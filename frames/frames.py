#!/usr/bin/python
# -*- coding: utf8 -*-

import sys, os
from random import shuffle

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import threading

from gamelib.game import *
from gamelib.animation import *
from gamelib.sound import *


GREY = [100, 100, 100]

# BIG TODO
# GAMEMODE? free field mus also be conquered
# prohibit 2 players on one field?


class Sounds:
    select = 'select'
    back = 'back'
    applause = 'aplause'
    occupy = 'occupy'
    occupy_error = 'occupy_error'
    win = 'win'
    cheer = 'cheer'
    countdown = 'countdown'


class Music:
    music_menu = 'music_menu'
    music_play = 'music_play'
    music_spiral = 'music_spiral'


class FramesGame(Game):
    def __init__(self, ip):
        Game.__init__(self, ip, [
            Sound(Sounds.select, 'sounds/menu_select.ogg'),
            Sound(Sounds.back, 'sounds/menu_back.ogg'),
            Sound(Sounds.applause, 'sounds/applause.ogg'),
            Sound(Sounds.occupy, 'sounds/occupy.ogg'),
            Sound(Sounds.occupy_error, 'sounds/occupy_error.ogg'),
            Sound(Sounds.win, 'sounds/win-oger.ogg'),
            Sound(Sounds.cheer, 'sounds/cheer.ogg'),
            Sound(Sounds.countdown, 'sounds/countdown.ogg'),
        ], [{
                "name": Music.music_menu,
                "file": 'sounds/music_menu.ogg',
                "volume": 0.5
            }, {
                "name": Music.music_play,
                "file": 'sounds/music_play.ogg',
                "volume": 0.5
            }, {
                "name": Music.music_spiral,
                "file": 'sounds/music_spiral.ogg',
                "volume": 1.0
            }])

        self.characterPositions = [
            Vector(0, 0),
            Vector(PIXEL_DIM_X - 1, 0),
            Vector(PIXEL_DIM_X - 1, PIXEL_DIM_Y - 1),
            Vector(0, PIXEL_DIM_Y - 1)
        ]

        self.boardColors = [RED, BLUE, GREEN, ORANGE, BLACK, WHITE]
        self.fadeColors = [RED, BLUE, GREEN, ORANGE, BLACK, WHITE]
        self.fadeAnimationRed = Animation(self.boardColors[0], BLACK, 0.3, AnimationLoopType.PingPong)
        self.fadeAnimationBlue = Animation(self.boardColors[1], BLACK, 0.3, AnimationLoopType.PingPong)
        self.fadeAnimationGreen = Animation(self.boardColors[2], BLACK, 0.3, AnimationLoopType.PingPong)
        self.fadeAnimationYellow = Animation(self.boardColors[3], BLACK, 0.3, AnimationLoopType.PingPong)

        self.fadeAnimationWhite = Animation(BLACK, GREY, 1.5, AnimationLoopType.PingPong)
        self.onlyAnimatePlayer0 = True

        #CONFIG
        self.SelectedPlayers = 2
        self.SelectedBlockDensity = 0
        self.SelectedTurnbased = False
        self.ActivePlayerTurnbased = 0

        self.hasFreeField = True

        self.axisVectors = [Vector(0, 0), Vector(0, 0), Vector(0, 0), Vector(0, 0)]
        self.infvertAxisX = False

        self.characterSpeed = 10
        self.countdown = 0

        self.score = [0, 0, 0, 0]
        self.places = [0, 0, 0, 0]

        # spiral
        self.Dt = 0
        self.LastSpiralFillLower = False
        self.spiralNextFillPosLower = [0, 0]
        self.spiralNextFillPosHigher = [11, 7]
        self.spiralHasLeftToFill = True
        self.limitSpiral = [[0 for x in xrange(PIXEL_DIM_Y)] for x in xrange(PIXEL_DIM_X)]

        # 0 game start                        -> player 1 click
        # 1 choose players                    -> player 1 click
        # 2 choose blocked amount             -> player 1 click (button 2 is back)
        # 3 choose game mode (arcade or slow) -> player 1 click (button 2 is back)
        # 4 start count down
        # 5 play                              -> start button -> (button 2 is pause with exit)
        # 6 spiral
        # 7 Won ->sound                       -> no free fields
        # 8 Score (min seconds)-> push button -> timer +player click
        # 9 replay or config new              -> player 1 click
        self.gameState = 0
        self.mayEnterNextState = False

        self.gameStateUpdateFunc = {
            0: self.updateState0,
            1: self.updateState1,
            2: self.updateState2,
            3: self.updateState3,
            4: self.updateState4,
            5: self.updateState5,
            6: self.updateState6,
            7: self.updateState7,
            8: self.updateState8,
            9: self.updateState9,
        }

        self.gameStateDrawFunc = {
            0: self.drawState0,
            1: self.drawState1,
            2: self.drawState2,
            3: self.drawState3,
            4: self.drawState4,
            5: self.drawState5,
            6: self.drawState6,
            7: self.drawState7,
            8: self.drawState8,
            9: self.drawState9,
        }

        self.gameStateButtonFunc = {
            0: self.updateButton0,
            1: self.updateButton1,
            2: self.updateButton2,
            3: self.updateButton3,
            4: self.updateButton4,
            5: self.updateButton5,
            6: self.updateButton6,
            7: self.updateButton7,
            8: self.updateButton8,
            9: self.updateButton9,
        }
        self.printState = False
        self.newStateForDraw = True
        self.newStateForUpdate = True

        # 0-3 player fields
        # 4 blocked fields
        # 5 free
        self.gameBoard = [[5 for x in xrange(PIXEL_DIM_Y)] for x in xrange(PIXEL_DIM_X)]

        # # setup blocked
        # self.gameBoard[4][4] = 4
        # self.gameBoard[4][5] = 4
        # self.gameBoard[4][3] = 4
        # self.gameBoard[5][3] = 4
        # self.gameBoard[5][4] = 4
        #
        # #setup player 2 fields
        # self.gameBoard[1][3] = 1
        # self.gameBoard[1][4] = 1
        # self.gameBoard[1][5] = 1
        #
        # self.gameBoard[10][3] = 0
        # self.gameBoard[10][4] = 1
        # self.gameBoard[10][5] = 2
        # self.gameBoard[10][6] = 3

    def stateChange(self, newState):
        self.gameState = newState
        self.newStateForDraw = True
        self.newStateForUpdate = True


####################################################################################################

    def updateState0(self, dt):
        if self.printState:
            print "Update S:%i" % self.gameState

        if self.newStateForUpdate == True:
            self.newStateForUpdate = False
            self.music.play(Music.music_menu)

    def updateState1(self, dt):
        if self.printState:
            print "Update S:%i" % self.gameState

        if self.newStateForUpdate == True:
            self.newStateForUpdate = False
            self.SelectedPlayers = 4

    def updateState2(self, dt):
        if self.printState:
            print "Update S:%i" % self.gameState

    def updateState3(self, dt):
        if self.printState:
            print "Update S:%i" % self.gameState

    def updateState4(self, dt):
        if self.printState:
            print "Update S:%i" % self.gameState

        if self.newStateForUpdate == True:
            self.newStateForUpdate = False
            self.setBoard(5)
            self.countdown = 0
            timer = threading.Timer(1.0, self.onCountdownTimerTick)
            timer.start()
            self.music.stop()

        if self.countdown == 4:
            self.stateChange(5)

    def onCountdownTimerTick(self):
        self.countdown += 1
        if self.countdown < 5:
            timer = threading.Timer(1.0, self.onCountdownTimerTick)
            timer.start()
            if self.countdown < 4:
                self.playSound(Sounds.countdown)


    def updateState5(self, dt):
        if self.printState:
            print "Update S:%i" % self.gameState

        if self.newStateForUpdate == True:
            self.newStateForUpdate = False
            self.music.play(Music.music_play)

            self.SetUpGameBoard()
            self.ActivePlayerTurnbased = randrange(self.SelectedPlayers)

        self.hasFreeField = False
        for x in xrange(PIXEL_DIM_X):
            if self.hasFreeField is False:
                for y in xrange(PIXEL_DIM_Y):
                    if self.gameBoard[x][y] == 5:
                        self.hasFreeField = True
                        #print "found free %i " % x + " %i" % y
                        break

        #self.hasFreeField = False
        # self.setBoard(1)
        # self.gameBoard[2][2]= 5
        if self.hasFreeField is False:
            if self.SelectedTurnbased:
                self.stateChange(7)  #win
            else:
                self.stateChange(6)  #spiral


    def updateState6(self, dt):
        if self.printState:
            print "Update S:%i" % self.gameState

        if self.newStateForUpdate:
            self.newStateForUpdate = False
            self.LastSpiralFillLower = False
            self.spiralNextFillPosLower = [0, 0]
            self.spiralNextFillPosHigher = [11, 7]
            self.spiralHasLeftToFill = True
            self.Dt = 0.0
            self.music.play(Music.music_spiral)

        self.Dt += dt

        if self.Dt >= 0.3:
            self.Dt -= 0.3
            self.updateSpiral()

        if self.spiralHasLeftToFill == False:
            self.stateChange(7)

    def updateSpiral(self):
        if self.LastSpiralFillLower:
            #print "fill higher"
            #print "next Higher %i" % self.spiralNextFillPosHigher[0] + " %i" % self.spiralNextFillPosHigher[1]
            if self.limitSpiral[self.spiralNextFillPosHigher[0]][self.spiralNextFillPosHigher[1]] == 1:
                self.spiralHasLeftToFill = False

            self.limitSpiral[self.spiralNextFillPosHigher[0]][self.spiralNextFillPosHigher[1]] = 1
            self.spiralNextFillPosHigher[1] -= 1
            if self.spiralNextFillPosHigher[1] == -1:
                self.spiralNextFillPosHigher[0] -= 1
                self.spiralNextFillPosHigher[1] = 7

            self.LastSpiralFillLower = False

        else:
            #print "fill lower"
            #print "next lower %i" % self.spiralNextFillPosLower[0] + " %i" % self.spiralNextFillPosLower[1]
            if self.spiralNextFillPosLower[0] == 12 or self.limitSpiral[self.spiralNextFillPosLower[0]][self.spiralNextFillPosLower[1]] == 1:
                self.spiralHasLeftToFill = False
                return

            self.limitSpiral[self.spiralNextFillPosLower[0]][self.spiralNextFillPosLower[1]] = 1
            self.spiralNextFillPosLower[1] += 1
            if self.spiralNextFillPosLower[1] == PIXEL_DIM_Y:
                self.spiralNextFillPosLower[0] += 1
                self.spiralNextFillPosLower[1] = 0

            self.LastSpiralFillLower = True

    def updateState7(self, dt):
        if self.printState:
            print "Update S:%i" % self.gameState

        if self.newStateForUpdate:
            #TODO play sound
            timer = threading.Timer(6.0, self.onWinTimerTick)
            timer.start()
            self.newStateForUpdate = False
            self.music.stop()
            self.playSound(Sounds.win)


    def updateState8(self, dt):
        if self.printState:
            print "Update S:%i" % self.gameState

        if self.newStateForUpdate:
            self.newStateForUpdate = False
            self.playSound(Sounds.applause)

            #calculate score
            self.score = [0, 0, 0, 0]
            for x in xrange(PIXEL_DIM_X):
                for y in xrange(PIXEL_DIM_Y):
                    if self.gameBoard[x][y] < 4:
                        self.score[self.gameBoard[x][y]] += 1

            #calc places
            place = 1
            lastmax = -1
            self.places = [0, 0, 0, 0]
            for i in range(4):
                maximum = max(self.score)
                maxindex = self.score.index(maximum)
                print "max :%i" % maximum + " i: %i" % maxindex
                if maximum < lastmax:
                    place += 1

                lastmax = maximum
                print "lastmax :%i" % lastmax + " place: %i" % place
                if maximum > 0:
                    self.places[maxindex] = place
                    self.score[maxindex] = 0
                else:
                    #rest is sam place
                    for p in range(4):
                        if self.places[p] == 0:
                            self.places[p] = place

            timer = threading.Timer(3.0, self.onMayLeaveTimerTick)
            timer.start()
            self.mayEnterNextState = False
            print "%i " % self.places[0] + "%i " % self.places[1] + "%i " % self.places[2] + "%i " % self.places[3]

    def onMayLeaveTimerTick(self):
        self.mayEnterNextState = True

    def updateState9(self, dt):
        if self.printState:
            print "Update S:%i" % self.gameState

        if self.newStateForUpdate:
            self.newStateForUpdate = False
            self.music.play(Music.music_menu)


    def onWinTimerTick(self):
        self.stateChange(8)

    ####################################################################################################

    def clearBoard(self, rgb):
        self.setBoard(4)

    def setBoard(self, value):
        for x in xrange(PIXEL_DIM_X):
            for y in xrange(PIXEL_DIM_Y):
                self.gameBoard[x][y] = value

    def drawBoard(self, rgb):
        for x in xrange(PIXEL_DIM_X):
            for y in xrange(PIXEL_DIM_Y):
                pos = Vector(x, y)
                rgb.setPixel(pos, self.boardColors[self.gameBoard[x][y]])

    def drawSpiral(self, rgb):
        for x in xrange(PIXEL_DIM_X):
            for y in xrange(PIXEL_DIM_Y):
                if self.limitSpiral[x][y] == 1:
                    pos = Vector(x, y)
                    rgb.setPixel(pos, BLACK)

    def drawBoardOnlyPlayerFields(self, rgb):
        for x in xrange(PIXEL_DIM_X):
            for y in xrange(PIXEL_DIM_Y):
                if self.gameBoard[x][y] < 4:
                    pos = Vector(x, y)
                    rgb.setPixel(pos, self.boardColors[self.gameBoard[x][y]])

    def drawPlayersArcade(self, rgb):
        for p in range(self.playerCount + 1):
            if p < self.SelectedPlayers:
                rgb.setPixel(self.characterPositions[p], self.fadeColors[p])

    def drawPlayersTurnbased(self, rgb):
        rgb.setPixel(self.characterPositions[self.ActivePlayerTurnbased], self.fadeColors[self.ActivePlayerTurnbased])

    def drawState0(self, rgb):
        if self.printState:
            print "%i" % self.gameState

        if self.newStateForDraw:
            self.clearBoard(rgb)
            self.newStateForDraw = False

        # cross
        self.gameBoard[5][4] = 5
        self.gameBoard[6][4] = 5
        self.gameBoard[7][4] = 5
        self.gameBoard[6][3] = 5
        self.gameBoard[6][5] = 5
        self.gameBoard[5][3] = 5
        self.gameBoard[5][5] = 5
        self.gameBoard[4][4] = 5

        self.drawBoard(rgb)
        self.drawPlayersArcade(rgb)

    def drawState1(self, rgb):
        if self.printState:
            print "Draw S:%i" % self.gameState

        if self.newStateForDraw:
            self.clearBoard(rgb)
            self.newStateForDraw = False
            self.onlyAnimatePlayer0 = True

        #2 player
        self.gameBoard[1][4] = 0
        self.gameBoard[2][3] = 1

        #3 player
        self.gameBoard[5][3] = 0
        self.gameBoard[6][3] = 1
        self.gameBoard[5][4] = 2

        #4 player
        self.gameBoard[9][3] = 0
        self.gameBoard[10][3] = 1
        self.gameBoard[9][4] = 2
        self.gameBoard[10][4] = 3

        #draw selection area
        color = self.fadeAnimationWhite.getValue()
        for x in [1, 2, 5, 6, 9, 10]:
            for y in range(PIXEL_DIM_Y):
                rgb.setPixel(Vector(x, y), color)

        self.drawBoardOnlyPlayerFields(rgb)
        self.drawPlayersArcade(rgb)

    def drawState2(self, rgb):
        if self.printState:
            print "Draw S:%i" % self.gameState

        if self.newStateForDraw:
            self.setBoard(5)
            self.newStateForDraw = False
            self.onlyAnimatePlayer0 = True

        #no blocked

        #light
        self.gameBoard[6][3] = 4
        self.gameBoard[5][5] = 4
        self.gameBoard[6][7] = 4

        #heavy
        self.gameBoard[9][2] = 4
        self.gameBoard[9][3] = 4
        self.gameBoard[10][3] = 4
        self.gameBoard[9][6] = 4
        self.gameBoard[10][4] = 4
        self.gameBoard[10][7] = 4

        self.drawBoard(rgb)

        #draw selection area
        color = self.fadeAnimationWhite.getValue()
        for x in [1, 2, 5, 6, 9, 10]:
            for y in range(PIXEL_DIM_Y):
                if self.gameBoard[x][y] != 4:
                    rgb.setPixel(Vector(x, y), color)

        self.drawPlayersArcade(rgb)

    def drawState3(self, rgb):
        if self.printState:
            print "Draw S:%i" % self.gameState

        if self.newStateForDraw:
            self.setBoard(4)
            self.newStateForDraw = False
            self.onlyAnimatePlayer0 = False

        self.drawBoard(rgb)

        # turn based
        #self.gameBoard[1][4] = 0 #animate

        self.gameBoard[1][3] = 1
        self.gameBoard[2][3] = 2
        self.gameBoard[2][4] = 3

        #4 arcade

        # self.gameBoard[9][3]  = 0
        # self.gameBoard[9][4]  = 1
        # self.gameBoard[10][3] = 2
        # self.gameBoard[10][4] = 3

        #draw selection area
        color = self.fadeAnimationWhite.getValue()
        for x in [1, 2, 9, 10]:
            for y in range(PIXEL_DIM_Y):
                if self.gameBoard[x][y] > 3:
                    rgb.setPixel(Vector(x, y), WHITE)

        rgb.setPixel(Vector(1, 4), self.fadeColors[0])
        rgb.setPixel(Vector(9, 3), self.fadeColors[0])
        rgb.setPixel(Vector(9, 4), self.fadeColors[1])
        rgb.setPixel(Vector(10, 3), self.fadeColors[2])
        rgb.setPixel(Vector(10, 4), self.fadeColors[3])

        #draw players
        rgb.setPixel(self.characterPositions[0], self.fadeColors[0])
        rgb.setPixel(self.characterPositions[1], self.boardColors[1])
        rgb.setPixel(self.characterPositions[2], self.boardColors[2])
        rgb.setPixel(self.characterPositions[3], self.boardColors[3])

    def drawState4(self, rgb):
        if self.printState:
            print "Draw S:%i" % self.gameState

        if self.newStateForDraw:
            self.newStateForDraw = False
            self.onlyAnimatePlayer0 = False
            self.setBoard(4)

        if self.countdown == 1:
            self.gameBoard[1][3] = 2
            self.gameBoard[1][4] = 2
            self.gameBoard[2][3] = 2
            self.gameBoard[2][4] = 2

        if self.countdown == 2:
            self.gameBoard[5][3] = 2
            self.gameBoard[5][4] = 2
            self.gameBoard[6][3] = 2
            self.gameBoard[6][4] = 2

        if self.countdown == 3:
            self.gameBoard[9][3] = 2
            self.gameBoard[9][4] = 2
            self.gameBoard[10][3] = 2
            self.gameBoard[10][4] = 2

        self.drawBoard(rgb)
        self.drawPlayersArcade(rgb)

    def drawState5(self, rgb):
        if self.printState:
            print "Draw S:%i" % self.gameState

        if self.newStateForDraw:
            self.newStateForDraw = False
            self.onlyAnimatePlayer0 = False

        self.drawBoard(rgb)
        if self.SelectedTurnbased == True:
            self.drawPlayersTurnbased(rgb)
        else:
            self.drawPlayersArcade(rgb)

    def drawState6(self, rgb):
        if self.printState:
            print "Draw S:%i" % self.gameState

        self.drawBoard(rgb)
        self.drawSpiral(rgb)
        self.drawPlayersArcade(rgb)

    def drawState7(self, rgb):
        if self.printState:
            print "Draw S:%i" % self.gameState

        if self.newStateForDraw:
            self.newStateForDraw = False
            self.onlyAnimatePlayer0 = False
            #self.setBoard(4)
            print "WIN"

        self.drawBoard(rgb)
        self.drawPlayersArcade(rgb)

    def drawState8(self, rgb):
        if self.printState:
            print "Draw S:%i" % self.gameState

        if self.newStateForDraw:
            self.newStateForDraw = False
            self.setBoard(4)
            # places
            # self.places = [1, 2, 2, 4]
            # self.SelectedPlayers = 4
            for p in range(self.SelectedPlayers):
                for height in range(5 - self.places[p]):
                    self.gameBoard[1 + p * 3][height + 2] = p
                    self.gameBoard[2 + p * 3][height + 2] = p

        self.drawBoard(rgb)

    def drawState9(self, rgb):
        if self.printState:
            print "Draw S:%i" % self.gameState

        if self.newStateForDraw:
            self.newStateForDraw = False
            self.setBoard(5)
            self.onlyAnimatePlayer0

        #OK
        self.gameBoard[0][3] = 2
        self.gameBoard[1][2] = 2
        self.gameBoard[2][3] = 2
        self.gameBoard[3][4] = 2
        self.gameBoard[4][5] = 2

        for y in range(PIXEL_DIM_Y):
            self.gameBoard[5][y] = 4
            self.gameBoard[6][y] = 4

        #back
        self.gameBoard[8][2] = 0
        self.gameBoard[9][3] = 0
        self.gameBoard[10][4] = 0
        self.gameBoard[8][4] = 0
        self.gameBoard[10][2] = 0

        self.drawBoard(rgb)
        self.drawPlayersArcade(rgb)

    ####################################################################################################
    def updateButton0(self, player, aButton, bButton, previousAButton, previousBButton):
        if self.printState:
            print "Button S:%i" % self.gameState

        if aButton == True and previousAButton == False:
            self.stateChange(1)
            self.playSound(Sounds.select)

    def updateButton1(self, player, aButton, bButton, previousAButton, previousBButton):
        if self.printState:
            print "Button S:%i" % self.gameState

        #back
        if bButton == True and previousBButton == False and player == 0:
            self.stateChange(0)
            self.playSound(Sounds.back)

        #select player
        if aButton == True and previousAButton == False and player == 0:
            if int(self.characterPositions[0].x) in {1, 2}:
                self.SelectedPlayers = 2
                self.stateChange(2)
            elif int(self.characterPositions[0].x) in {5, 6}:
                self.SelectedPlayers = 3
                self.stateChange(2)
            elif int(self.characterPositions[0].x) in {9, 10}:
                self.SelectedPlayers = 4
                self.stateChange(2)
            self.playSound(Sounds.cheer)


    def updateButton2(self, player, aButton, bButton, previousAButton, previousBButton):
        if self.printState:
            print "Button S:%i" % self.gameState

        #back
        if bButton == True and previousBButton == False and player == 0:
            self.stateChange(1)
            self.playSound(Sounds.back)

        #select density
        if aButton == True and previousAButton == False and player == 0:
            if int(self.characterPositions[0].x) in {1, 2}:
                self.SelectedBlockDensity = 0
                self.stateChange(3)
            elif int(self.characterPositions[0].x) in {5, 6}:
                self.SelectedBlockDensity = 1
                self.stateChange(3)
            elif int(self.characterPositions[0].x) in {9, 10}:
                self.SelectedBlockDensity = 2
                self.stateChange(3)
            self.playSound(Sounds.select)


    def updateButton3(self, player, aButton, bButton, previousAButton, previousBButton):
        if self.printState:
            print "Button S:%i" % self.gameState

        #back
        if bButton == True and previousBButton == False and player == 0:
            self.stateChange(2)

        #select density
        if aButton == True and previousAButton == False and player == 0:
            if int(self.characterPositions[0].x) in {1, 2}:
                self.SelectedTurnbased = True
                self.stateChange(4)
            elif int(self.characterPositions[0].x) in {9, 10}:
                self.SelectedTurnbased = False
                self.stateChange(4)
            self.playSound(Sounds.select)

    def updateButton4(self, player, aButton, bButton, previousAButton, previousBButton):
        if self.printState:
            print "Button S:%i" % self.gameState

    def updateButton5(self, player, aButton, bButton, previousAButton, previousBButton):
        if self.printState:
            print "Button S:%i" % self.gameState

        if self.SelectedTurnbased == True and player != self.ActivePlayerTurnbased:
            return

        if aButton == True and previousAButton == False:
            posx = "%i" % self.characterPositions[player].x
            posy = "%i" % self.characterPositions[player].y
            #print "player: " + "%i" % player + " occupied " + posx + " / " + posy

            cx = int(self.characterPositions[player].x)
            cy = int(self.characterPositions[player].y)
            # not blocked
            gotField = False
            if self.gameBoard[cx][cy] < 4:  #is occupied
                #print "%i / " % cx + "%i" % cy
                neighbours = [0, 0, 0, 0]
                if cy > 0 and self.gameBoard[cx][cy - 1] < 4: neighbours[self.gameBoard[cx][cy - 1]] += 1
                if self.gameBoard[cx][cy] < 4: neighbours[self.gameBoard[cx][cy]] += 1
                if cy < 7 and self.gameBoard[cx][cy + 1] < 4: neighbours[self.gameBoard[cx][cy + 1]] += 1
                if cx > 0 and cy > 0 and self.gameBoard[cx - 1][cy - 1] < 4: neighbours[self.gameBoard[cx - 1][cy - 1]] += 1
                if cx > 0 and self.gameBoard[cx - 1][cy] < 4: neighbours[self.gameBoard[cx - 1][cy]] += 1
                if cx > 0 and cy < 7 and self.gameBoard[cx - 1][cy + 1] < 4: neighbours[self.gameBoard[cx - 1][cy + 1]] += 1
                if cx < 11 and cy > 0 and self.gameBoard[cx + 1][cy - 1] < 4: neighbours[self.gameBoard[cx + 1][cy - 1]] += 1
                if cx < 11 and self.gameBoard[cx + 1][cy] < 4: neighbours[self.gameBoard[cx + 1][cy]] += 1
                if cx < 11 and cy < 7 and self.gameBoard[cx + 1][cy + 1] < 4: neighbours[self.gameBoard[cx + 1][cy + 1]] += 1
                # print "N: " + "%i" % neighbours[0] + "%i" % neighbours[1] + "%i" % neighbours[2] + "%i" % neighbours[3]

                isbiggest = True;
                for p in range(self.playerCount):
                    # print "%i" % player + "%i" % p + "%i" % self.playerCount
                    # print "%i" % neighbours[player] + "%i" % neighbours[p]
                    if neighbours[player] <= neighbours[p] and player != p:
                        #print "no"
                        isbiggest = False

                if isbiggest:
                    self.gameBoard[int(self.characterPositions[player].x)][int(self.characterPositions[player].y)] = player
                    gotField = True

            elif self.gameBoard[cx][cy] == 5:  # is free
                self.gameBoard[int(self.characterPositions[player].x)][int(self.characterPositions[player].y)] = player
                gotField = True

            if gotField == True:
                self.playSound(Sounds.occupy)
                if self.SelectedTurnbased == True:
                    self.selectNextActivePlayer()
            else:
                self.playSound(Sounds.occupy_error)

    def selectNextActivePlayer(self):
        self.ActivePlayerTurnbased = (self.ActivePlayerTurnbased + 1) % self.SelectedPlayers

    def updateButton6(self, player, aButton, bButton, previousAButton, previousBButton):
        if self.printState:
            print "Button S:%i" % self.gameState

        if self.limitSpiral[int(self.characterPositions[player].x)][int(self.characterPositions[player].y)] == 1:
            self.playSound(Sounds.occupy_error)
            return

        self.updateButton5(player, aButton, bButton, previousAButton, previousBButton)

    def updateButton7(self, player, aButton, bButton, previousAButton, previousBButton):
        if self.printState:
            print "Button S:%i" % self.gameState

    def updateButton8(self, player, aButton, bButton, previousAButton, previousBButton):
        if self.printState:
            print "Button S:%i" % self.gameState

        if self.mayEnterNextState == True and aButton == True and previousAButton == False:
            self.playSound(Sounds.select)
            self.stateChange(9)

    def updateButton9(self, player, aButton, bButton, previousAButton, previousBButton):
        if self.printState:
            print "Button S:%i" % self.gameState

        if aButton == True and previousAButton == False and player == 0:
            if int(self.characterPositions[0].x) < 5:
                self.SelectedTurnbased = True
                self.stateChange(4)
                self.playSound(Sounds.select)
            elif int(self.characterPositions[0].x) > 6:
                self.SelectedTurnbased = False
                self.stateChange(0)
                self.playSound(Sounds.select)
        self.onlyAnimatePlayer0 = False


    def update(self, dt):
        Game.update(self, dt)

        self.fadeAnimationRed.update(dt)
        if self.onlyAnimatePlayer0 is False:
            self.fadeAnimationBlue.update(dt)
            self.fadeAnimationGreen.update(dt)
            self.fadeAnimationYellow.update(dt)

        self.fadeAnimationWhite.update(dt)

        for player in range(self.playerCount):
            playerPos = self.characterPositions[player] + ( self.axisVectors[player] * dt ) * self.characterSpeed
            self.characterPositions[player] = Vector(playerPos.x % PIXEL_DIM_X, playerPos.y % PIXEL_DIM_Y)

        self.gameStateUpdateFunc[self.gameState](dt)

    def draw(self, rgb):
        Game.draw(self, rgb)

        self.fadeColors[0] = self.fadeAnimationRed.getValue()
        self.fadeColors[1] = self.fadeAnimationBlue.getValue()
        self.fadeColors[2] = self.fadeAnimationGreen.getValue()
        self.fadeColors[3] = self.fadeAnimationYellow.getValue()

        self.gameStateDrawFunc[self.gameState](rgb)

    def onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis):
        Game.onAxisChanged(self, player, xAxis, yAxis, previousXAxis, previousYAxis)

        if self.infvertAxisX:
            self.axisVectors[player] = Vector(-xAxis, yAxis)
        else:
            self.axisVectors[player] = Vector(xAxis, yAxis)

    def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
        Game.onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton)

        if player >= self.SelectedPlayers:
            return


        self.gameStateButtonFunc[self.gameState](player, aButton, bButton, previousAButton, previousBButton)
        #print "onButtonChanged"

    def SetUpGameBoard(self):
        self.setBoard(5)

        if self.SelectedBlockDensity == 0:
            return
        elif self.SelectedBlockDensity == 1:
            probability = 0.18
        elif self.SelectedBlockDensity == 2:
            probability = 0.33

        for x in xrange(PIXEL_DIM_X):
            for y in xrange(PIXEL_DIM_Y):
                if random() < probability:
                    self.gameBoard[x][y] = 4
                    #print "Blocked at %i" % x + "%i" % y


if __name__ == "__main__":
    print "Starting game"
    game = FramesGame("192.168.0.17")
    game.run()
    print "Stopping game"

