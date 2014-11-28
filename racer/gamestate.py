#!/usr/bin/python
# -*- coding: utf8 -*-

from gamelib.game import *
from gamelib.sprites.explosion import *

import random
from gamelib.state import State

from ship import Ship


class GameState(State):

    def __init__(self):
        State.__init__(self, "Game")

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

        self.simulationPause = False

        self.sprites = []

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
        State.update(self, dt)

        self.offset += self.scroll_speed * dt
        self.scroll_speed += self.scroll_speed_increment * dt

        if self.offset >= 1.0:
            while self.offset >= 1.0:
                self.offset -= 1.0

            self.check_collision()

            del self.map[0]
            self.map.append(self.generate_map_slice())

        self.ship.update(dt)
        self.ship.animation.duration = 1.0/self.scroll_speed

        self.sprites = [sprite for sprite in self.sprites if not sprite.ended]
        for sprite in self.sprites:
            sprite.update(dt)

    def draw(self, rgb):
        State.draw(self, rgb)

        for y in range(PIXEL_DIM_Y):
            left, right = self.map[y][0], self.map[y][1]

            for lx in range(left):
                pixel = Vector(lx, y)
                rgb.setPixel(pixel, self.wall_color)
            for rx in range(right):
                pixel = Vector(PIXEL_DIM_X - 1 - rx, y)
                rgb.setPixel(pixel, self.wall_color)

        self.ship.draw(rgb)

        for sprite in self.sprites:
            sprite.draw(rgb)

    @staticmethod
    def draw_pixel_at(rgb, position, color):
        x_rest = position.x % 1
        y_rest = position.y % 1

        rest = math.sqrt(x_rest*x_rest + y_rest*y_rest)

        rgb.add_color(position + Vector(1, 0), Color.multiply(color, x_rest))
        rgb.add_color(position + Vector(0, 1), Color.multiply(color, y_rest))

        rgb.add_color(position, Color.multiply(color, 1 - rest))

    def onClampedAxisChanged(self, player, x, y):
        State.onClampedAxisChanged(self, player, x, y)
        self.ship.position.x += x

    def onButtonChanged(self, player, a_button, b_button, previous_a_button, previous_b_button):
        State.onButtonChanged(self, player, a_button, b_button, previous_a_button, previous_b_button)

    def check_collision(self):
        relevant_slice = self.map[2]

        if relevant_slice[0] > self.ship.position.x or \
           PIXEL_DIM_X - 1 - relevant_slice[1] < self.ship.position.x:
            print "collide!", time.time()
            self.add_explosion(self.ship.position)
            #todo explode, sound, score, next player
            
            self.game_over()

    def add_explosion(self, position):
        explosion = Explosion(position)
        self.sprites.append(explosion)
        #self.playSound(Sounds.explode)

        self.simulationPause = explosion.duration

    def game_over(self):
        pass

    @staticmethod
    def draw_pixel_at(rgb, position, color):
        x_rest = position.x % 1
        y_rest = position.y % 1

        rest = math.sqrt(x_rest*x_rest + y_rest*y_rest)

        rgb.add_color(position + Vector(1, 0), Color.multiply(color, x_rest))
        rgb.add_color(position + Vector(0, 1), Color.multiply(color, y_rest))

        rgb.add_color(position, Color.multiply(color, 1 - rest))