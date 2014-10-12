#!/usr/bin/python
# -*- coding: utf8 -*- 

import pygame, os, sys, time, math, socket, select
import pygame.font
from pygame.color import Color
from random import *

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'gamelib'))
from vector import *

import pygl2d
from pygl2d.font import RenderText

PING_INTERVALL = 3.0
FREQ = 44100
BITSIZE = -16
CHANNELS = 2
BUFFER = 1024
FRAMERATE = 30
FULLSCREEN = False
SOUND = False

PIXEL_SIZE = 3
PIXEL_DIM_Y = 8
PIXEL_DIM_X = 12

class SimulatorMain:
	
	def __init__(self, ip):
		self.UDP_IP = ip
		self.UDP_PORT = 6803

		self.screen = None
		self.screenDim = Vector(800,576)
		self.background = (255,255,255)
		self.running = False
		self.showFPS = True
	
		flags = pygame.DOUBLEBUF | pygame.OPENGL
		if FULLSCREEN:
			flags |= pygame.FULLSCREEN
		pygl2d.window.init(self.screenDim.toIntArr(), caption="Couchtable Simulator v1.0", bg=(133.0/255.0, 94.0/255.0, 66.0/255.0, 1.0), flags=flags)

		pygame.font.init()
		fontname = pygame.font.get_default_font()
		self.font = pygame.font.Font(fontname, 32)

		self.music = None

		self.tilesX = 12
		self.tilesY = 8
		self.tileWidth = 50
		self.tileHeight = 50
		self.offsetLeft = 40
		self.offsetTop = 50
		self.gridMargin = 10
		self.gridData = []

		for x in range(self.tilesX):
			self.gridData.append([])
			for y in range(self.tilesY):
				self.gridData[x].append((0,0,0))


	# ====================================================================================================
	# =======================           Game Loop                    =====================================
	# ====================================================================================================
	
	def draw(self):
		pygl2d.window.begin_draw()

		if self.showFPS:
			fps = self.clock.get_fps()
			#print "FPS:",fps
			fps_display = pygl2d.font.RenderText(str(int(fps)), [0, 0, 0], self.font)
			fps_display.draw([10, 10])

		for x in range(self.tilesX):
			for y in range(self.tilesY):
				color = self.gridData[x][y]
				px = self.offsetLeft + x*self.tileWidth + x*self.gridMargin
				py = self.offsetTop + y*self.tileHeight + y*self.gridMargin
				pygl2d.draw.rect((px, py, px + self.tileWidth, py + self.tileHeight), color, 0, 255.0, False)

		pygl2d.window.end_draw()

	def readData(self, data):
		pixels_in_buffer = len(data) / PIXEL_SIZE
		pixels = bytearray(data)

		for i in range(pixels_in_buffer):
			pixel = (pixels[i*PIXEL_SIZE], pixels[i*PIXEL_SIZE+1], pixels[i*PIXEL_SIZE+2])

			y = i % PIXEL_DIM_Y
			x = int(math.floor(i / PIXEL_DIM_Y))

			if x % 2 == 0:
				self.gridData[x][y] = pixel
			else:
				self.gridData[x][(PIXEL_DIM_Y-1)-y] = pixel


	def run(self):
		print ("Start listener " + self.UDP_IP + ":" + str(self.UDP_PORT))
		sock = socket.socket( socket.AF_INET, # Internet
							  socket.SOCK_DGRAM ) # UDP
		sock.bind( (self.UDP_IP,self.UDP_PORT) )
		sock.settimeout(0.1)
		UDP_BUFFER_SIZE = 1024

		self.running = True
		self.clock = pygame.time.Clock()

		while self.running:
			#dt = self.clock.tick(30) / 1000.0
			data = None
			try:
				data, addr = sock.recvfrom( UDP_BUFFER_SIZE ) # blocking call
			except:
				pass

			if data:
				self.readData(data)

			self.draw()

if __name__ == '__main__':
	if "--debug" in sys.argv:
		DEBUG=True
		sys.argv.remove("--debug")

	if "--fullscreen" in sys.argv:
		FULLSCREEN=True
		sys.argv.remove("--fullscreen")

	main = SimulatorMain("127.0.0.1")
	print "starting..."
	main.run()
	print "shuting down..."
