# -*- coding: utf8 -*- 

class Resource(object):
    def __init__(self, name, resFile):
        self.name = name
        self.resFile = resFile

    def load(self):
        raise Exception('Not implemented')