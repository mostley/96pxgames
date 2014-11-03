# -*- coding: utf8 -*-

from random import *


class HeightMapData:
    def __init__(self, size):
        self.w = size
        self.h = size
        self.data = []
        for c in range(size+1):
            t = []
            for i in range(size+1):
                t.append(0)
            self.data.append(t)


class DiamondSquare:
    def __init__(self, width, height, f=None):
        self.width = width
        self.height = height
        self.func = f
        if not self.func:
            self.func = DiamondSquare.default_func

        # make heightmap
        self.heightmap = None
        self.init_heightmap(self.pot())

    def pot(self):
        size = max(self.width, self.height)
        result = 2

        while True:
            if size <= result:
                break
            result *= 2

        return result

    def square(self, x, y, d, f):
        """ Square step
            Sets map[x][y] from square of radius d using height function f"""

        heightmap = self.heightmap

        n_sum, num = 0, 0
        if 0 <= x - d:
            if 0 <= y - d:
                n_sum = n_sum + heightmap.data[x - d][y - d]
                num += 1

            if y + d <= heightmap.h:
                n_sum = n_sum + heightmap.data[x - d][y + d]
                num += 1

        if x + d <= heightmap.w:
            if 0 <= y - d:
                n_sum = n_sum + heightmap.data[x + d][y - d]
                num += 1
            if y + d <= heightmap.h:
                n_sum = n_sum + heightmap.data[x + d][y + d]
                num += 1

        heightmap.data[x][y] = f(heightmap, x, y, d, n_sum / num)

    def diamond(self, x, y, d, f):
        """ Diamond step
            Sets map[x][y] from diamond of radius d using height function f"""

        heightmap = self.heightmap

        n_sum, num = 0, 0
        if 0 <= x - d:
            n_sum = n_sum + heightmap.data[x - d][y]
            num += 1

        if x + d <= heightmap.w:
            n_sum = n_sum + heightmap.data[x + d][y]
            num += 1

        if 0 <= y - d:
            n_sum = n_sum + heightmap.data[x][y - d]
            num += 1

        if y + d <= heightmap.h:
            n_sum = n_sum + heightmap.data[x][y + d]
            num += 1

        heightmap.data[x][y] = f(heightmap, x, y, d, n_sum / num)

    def init_heightmap(self, size):
        """ Diamond square algorithm generates cloud/plasma fractal heightmap
            http://en.wikipedia.org/wiki/Diamond-square_algorithm
            :param size: must be power of two
        """

        # create map
        heightmap = self.heightmap = HeightMapData(size)

        # seed four corners
        d = size
        heightmap.data[0][0] = self.func(heightmap, 0, 0, d, 0)
        heightmap.data[0][d] = self.func(heightmap, 0, d, d, 0)
        heightmap.data[d][0] = self.func(heightmap, d, 0, d, 0)
        heightmap.data[d][d] = self.func(heightmap, d, d, d, 0)
        d /= 2

        # perform square and diamond steps
        while 1 <= d:
            for x in range(d, heightmap.w - 1, 2 * d):
                for y in range(d, heightmap.h - 1, 2 * d):
                    self.square(x, y, d, self.func)

            for x in range(d, heightmap.w - 1, 2 * d):
                for y in range(0, heightmap.h, 2 * d):
                    self.diamond(x, y, d, self.func)

            for x in range(0, heightmap.w, 2 * d):
                for y in range(d, heightmap.h - 1, 2 * d):
                    self.diamond(x, y, d, self.func)

            d /= 2

    @staticmethod
    def default_func(heightmap, x, y, d, h):
        """ Default height function
            :param heightmap: the map
            :param x: the x position
            :param y: the y position
            :param d: is depth (from size to 1 by powers of two)
            :param h: is mean height at map[x][y] (from square/diamond of radius d)
            :return: h' which is used to set map[x][y]
        """

        return h + (random()) * d

    # Create a heightmap using the specified height function (or default)
    # map[x][y] where x from 0 to map.w and y from 0 to map.h
    def create(self):
        heightmap = self.heightmap
        # clip heightmap to desired size
        for x in range(heightmap.w):
            for y in range(self.height + 1, heightmap.h):
                heightmap.data[x][y] = None
        for x in range(self.width + 1, heightmap.w):
            heightmap.data[x] = None

        heightmap.w, heightmap.h = self.width, self.height

        return heightmap