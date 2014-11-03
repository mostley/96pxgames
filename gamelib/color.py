
WHITE = [255,255,255]
RED = [255,0,0]
GREEN = [0,255,0]
BLUE = [0,0,255]
TURQUE = [0,255,255]
YELLOW = [255,255,0]
BLACK = [0,0,0]
ORANGE = [255, 127, 0]
PURPLE = [128, 0, 128]

class Color:
    @staticmethod
    def multiply(color, factor):
        return [ color[0] * factor, color[1] * factor, color[2] * factor ]