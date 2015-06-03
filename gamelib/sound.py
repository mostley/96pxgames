# -*- coding: utf8 -*- 

import pygame
from resource import Resource

class Sound(Resource):
    def __init__(self, name, resFile):
        Resource.__init__(self, name, resFile)

        self.sound = None

    def load(self):
        self.sound = pygame.mixer.Sound(self.resFile)

    def play(self):
        if self.sound == None:
            raise Exception("sound is not initialized, please call load first")

        self.sound.play()

    def stop(self):
        if self.sound == None:
            raise Exception("sound is not initialized, please call load first")
        
        self.sound.stop()

    def fadeout(self, time):
        if self.sound == None:
            raise Exception("sound is not initialized, please call load first")
        
        self.sound.fadeout(time)