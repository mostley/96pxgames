# -*- coding: utf8 -*- 

import pygame


class KeyboardController(object):
    def __init__(self, controller_id):
        if controller_id == 0:
            self.leftKey = pygame.K_LEFT
            self.rightKey = pygame.K_RIGHT
            self.upKey = pygame.K_UP
            self.downKey = pygame.K_DOWN
            self.button0 = pygame.K_i
            self.button1 = pygame.K_o
            self.button2 = pygame.K_k
            self.button3 = pygame.K_l
        if controller_id == 1:
            self.leftKey = pygame.K_a
            self.rightKey = pygame.K_d
            self.upKey = pygame.K_w
            self.downKey = pygame.K_s
            self.button0 = pygame.K_r
            self.button1 = pygame.K_t
            self.button2 = pygame.K_f
            self.button3 = pygame.K_g

        self.events = {
            self.leftKey:  False,
            self.rightKey: False,
            self.upKey:    False,
            self.downKey:  False,
            self.button0:  False,
            self.button1:  False,
            self.button2:  False,
            self.button3:  False,
        }

    def set_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.events[event.key] = True
            if event.type == pygame.KEYUP:
                self.events[event.key] = False

    def get_axis(self, axis):
        result = 0

        if axis == 0:
            if self.events[self.leftKey]:
                result += 1
            if self.events[self.rightKey]:
                result -= 1
        if axis == 1:
            if self.events[self.upKey]:
                result -= 1
            if self.events[self.downKey]:
                result += 1

        return result

    def get_button(self, button_index):
        result = False

        if self.events[self.button0]:
            result = button_index == 0
        elif self.events[self.button1]:
            result = button_index == 1
        elif self.events[self.button2]:
            result = button_index == 2
        elif self.events[self.button3]:
            result = button_index == 3

        return result

