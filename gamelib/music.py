# -*- coding: utf8 -*- 

import pygame

class MusicManager(object):
    def __init__(self, songs):
        self.songs = {}
        for song in songs:
            self.songs[song["name"]] = song
            self.songs[song["name"]]["position"] = 0

        self.loadedSong = None

    def play(self, name):
        if self.loadedSong != name:
            if self.loadedSong != None:
                self.songs[self.loadedSong]["position"] = pygame.mixer.music.get_pos()
            pygame.mixer.music.load(self.songs[name]["file"])
            if self.songs[name].has_key('volume'):
                pygame.mixer.music.set_volume(self.songs[name]["volume"])
            self.loadedSong = name

        pygame.mixer.music.play(-1, self.songs[name]["position"]/1000)

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.stop()

    def fadeout(self, time):
        pygame.mixer.music.fadeout(time)