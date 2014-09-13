# -*- coding: utf8 -*- 

import pygame

class KeyboardController:
	def __init__(self, id):
		if id == 0:
			self.leftKey = pygame.K_LEFT
			self.rightKey = pygame.K_RIGHT
			self.upKey = pygame.K_UP
			self.downKey = pygame.K_DOWN
			self.button0 = pygame.K_i
			self.button1 = pygame.K_o
			self.button2 = pygame.K_k
			self.button3 = pygame.K_l
		if id == 1:
			self.leftKey = pygame.K_a
			self.rightKey = pygame.K_d
			self.upKey = pygame.K_w
			self.downKey = pygame.K_s
			self.button0 = pygame.K_r
			self.button1 = pygame.K_t
			self.button2 = pygame.K_f
			self.button3 = pygame.K_g
			
		self.events = []
		
	def set_events(self, events):
		self.events = events
		
	def get_axis(self, axis):
		result = 0
		
		for event in self.events:
			if event.type == pygame.KEYDOWN :
				if axis == 0:
					if event.key == self.leftKey:
						result += 1
					elif event.key == self.rightKey:
						result -= 1
				if axis == 1:
					if event.key == self.upKey:
						result -= 1
					elif event.key == self.downKey:
						result += 1
		
		return result
	
	def get_button(self, buttonIndex):
		result = False
		
		for event in self.events:
			if event.type == pygame.KEYDOWN :
				if event.key == self.button0:
					result = buttonIndex  == 0
					break
				elif event.key == self.button1:
					result = buttonIndex  == 1
					break
				elif event.key == self.button2:
					result = buttonIndex  == 2
					break
				elif event.key == self.button3:
					result = buttonIndex  == 3
					break
		
		return result
		
		