#!/usr/bin/python
# -*- coding: utf8 -*- 

import sys, socket, math
from vector import *
from color import *
from flaschen import FlaschenDevice

PIXEL_SIZE = 3
PIXEL_DIM_X = 45
PIXEL_DIM_Y = 35
BUFFER_SIZE = PIXEL_DIM_X * PIXEL_DIM_Y * PIXEL_SIZE

def clampByte(i): return 1 if i < 1 else ( i if i < 256 else 255 )

class RGB(object):

    def __init__(self, ip='ft.noise', port=1337, verbose=False):
        print "Connecting to ", ip, ":", port
        self.UDP_IP = ip
        self.UDP_PORT = port
        self.verbose = verbose
        self.invertedX = False
        self.invertedY = False
        self.remote = self.UDP_IP != None

        self.device = FlaschenDevice(self.UDP_IP, self.UDP_PORT, PIXEL_DIM_X, PIXEL_DIM_Y)

    # ==================================================================================================
    # ====================      Private                       ==========================================
    # ==================================================================================================

    def _writeBytes(self, bytedata):
        self.device.write(bytedata)

    def _colorEquals(self, c1, c2):
        return c1[0] == c2[0] and c1[1] == c2[1] and c1[2] == c2[2]

    def _get_coord(self, v):
        result = None

        pos = v.toIntArr()
        if self.invertedX:
            pos[0] = (PIXEL_DIM_X - 1) - pos[0]
        if self.invertedY:
            pos[1] = (PIXEL_DIM_Y - 1) - pos[1]
        if 0 <= pos[0] < PIXEL_DIM_X and 0 <= pos[1] < PIXEL_DIM_Y:
            result = pos

        return result

    # ==================================================================================================
    # ====================      Public                         ==========================================
    # ==================================================================================================

    def add_color(self, v, color):
        pos = self._get_coord(v)
        if not pos is None:
            new_color = Color.add(color, self.buffer[pos[0]][pos[1]])
            self.setPixel(v, new_color)

    def mix_color(self, v, color, alpha):
        pos = self._get_coord(v)
        if not pos is None:
            new_color = Color.add(Color.multiply(color, alpha), self.buffer[pos[0]][pos[1]])
            self.setPixel(v, new_color)

    def setPixel(self, v, color):
        #print v,color
        if color is None or len(color) < 3:
            raise Exception("wrong color format " + str(color))

        pos = self._get_coord(v)
        if not pos is None:
            self.device.set(pos[0], pos[1], color)

    def clear(self, color):
        for x in range(PIXEL_DIM_X):
            for y in range(PIXEL_DIM_Y):
                self.device.set(x, y, color)

    def send(self):
        if self.verbose:
            print "sending to ",self.UDP_IP,":",self.UDP_PORT
            print "sending ",self.device._data

        self.device.send()


