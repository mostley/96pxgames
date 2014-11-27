#!/usr/bin/python
# -*- coding: utf8 -*-
from gamelib.animatedgameobject import AnimatedGameObject

from gamelib.game import *
import random


class Ship(AnimatedGameObject):
    def __init__(self, position, color1, color2):
        AnimatedGameObject.__init__(self, position, color1, color2)

        self.outer_color_fraction = 0.2
        self.speed = 5
        self.friction = 1.0

    def update(self, dt):
        AnimatedGameObject.update(self, dt)

    def draw(self, rgb):

        outer_color = Color.multiply(YELLOW, self.outer_color_fraction)

        rgb.setPixel(self.position, self.color)
        rgb.mix_color(self.position + Vector(0, -1).toIntArr(), YELLOW, 1)
        rgb.mix_color(self.position + Vector(-1, -1).toIntArr(), YELLOW, 0.1)
        rgb.mix_color(self.position + Vector(1, -1).toIntArr(), YELLOW, 0.1)


class Racer(Game):

    def __init__(self, ip):
        Game.__init__(self, ip)

        self.characterPosition = Vector(5, 7)

        self.character_colors = [RED, BLUE, WHITE, ORANGE, PURPLE]
        self.background_color = BLACK
        self.wall_color = Color.multiply(GREEN, 0.5)

        self.map = []
        self.offset = 0.0
        self.scroll_speed = 0.5
        self.scroll_speed_increment = 0.1
        self.sharpness = 1.1

        self.ship_steer_speed = 0.1

        self.ship = Ship(Vector(6, 1), self.character_colors[0], Color.multiply(self.character_colors[0], 0.8))

        for y in range(PIXEL_DIM_Y*2 + 1):
            self.map.append(self.generate_map_slice())

    def generate_map_slice(self):
        if len(self.map) == 0:
            left = random.choice(range(6))
            right = random.choice(range(6))
        else:
            last_slice = self.map[-1]

            left = last_slice[0] + random.choice([-1, 0, 1])
            right = last_slice[1] + random.choice([-1, 0, 1])

            left = left if 0 <= left < PIXEL_DIM_X else last_slice[0]
            right = right if 0 <= right < PIXEL_DIM_X else last_slice[1]

            while (left + right) >= (PIXEL_DIM_X - 1):
                if random.choice([0, 1]) == 0:
                    left -= 1
                else:
                    right -= 1

        return [left, right]

    def update(self, dt):
        Game.update(self, dt)

        self.offset += self.scroll_speed * dt
        self.scroll_speed += self.scroll_speed_increment * dt

        if self.offset >= 1.0:
            while self.offset >= 1.0:
                self.offset -= 1.0

            self.check_collision()

            del self.map[0]
            self.map.append(self.generate_map_slice())

        self.ship.update(dt)

    def draw(self, rgb):
        Game.draw(self, rgb)

        for y in range(PIXEL_DIM_Y):
            left, right = self.map[y][0], self.map[y][1]
            next_left, next_right = self.map[y+1]


            for lx in range(left):
                pixel = Vector(lx, y)
                rgb.setPixel(pixel, self.wall_color)
            for rx in range(right):
                pixel = Vector(PIXEL_DIM_X - 1 - rx, y)
                rgb.setPixel(pixel, self.wall_color)

        self.ship.draw(rgb)

    @staticmethod
    def draw_pixel_at(rgb, position, color):
        x_rest = position.x % 1
        y_rest = position.y % 1

        rest = math.sqrt(x_rest*x_rest + y_rest*y_rest)

        rgb.add_color(position + Vector(1, 0), Color.multiply(color, x_rest))
        rgb.add_color(position + Vector(0, 1), Color.multiply(color, y_rest))

        rgb.add_color(position, Color.multiply(color, 1 - rest))

    def onClampedAxisChanged(self, player, x, y):
        Game.onClampedAxisChanged(self, player, x, y)
        self.ship.position.x += x

    def onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton):
        Game.onButtonChanged(self, player, aButton, bButton, previousAButton, previousBButton)

    def check_collision(self):
        relevant_slice = self.map[1]

        if relevant_slice[0] > self.ship.position.x or \
           PIXEL_DIM_X - 1 - relevant_slice[1] <= self.ship.position.x:
            print "collide!", time.time()
            #todo explode, sound, score, next player


if __name__ == "__main__":
    print "Starting game"
    #ip = "127.0.0.1"
    ip = "192.168.0.19"
    if len(sys.argv) > 1:
        ip = sys.argv[1]
    game = Racer(ip)
    game.run()
    print "Stopping game"

