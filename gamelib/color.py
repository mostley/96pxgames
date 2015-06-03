WHITE = [255, 255, 255]
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
TURQUE = [0, 255, 255]
YELLOW = [255, 255, 0]
BLACK = [0, 0, 0]
ORANGE = [255, 127, 0]
PURPLE = [128, 0, 128]


class Color(object):
    @staticmethod
    def multiply(color, factor):
        return [color[0] * factor, color[1] * factor, color[2] * factor]

    @staticmethod
    def add(color, other_color):
        return [color[0] + other_color[0], color[1] + other_color[1], color[2] + other_color[2]]
