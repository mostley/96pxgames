# -*- coding: utf8 -*- 

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from gamelib.sprite import *
from gamelib.vector import *
from gamelib.animation import *

class Explosion(Sprite):
	def __init__(self, position):
		self.duration = 0.5

		sprite1 = [
			{ 'position': Vector( 0, 0), 'color': RED },
			{ 'position': Vector(-1, 0), 'color': RED },
			{ 'position': Vector( 1, 0), 'color': RED },
			{ 'position': Vector( 0,-1), 'color': RED },
			{ 'position': Vector( 0, 1), 'color': RED }
		]
		sprite2 = [
			{ 'position': Vector(-1,-1), 'color': RED },
			{ 'position': Vector( 0,-1), 'color': RED },
			{ 'position': Vector( 1,-1), 'color': RED },
			{ 'position': Vector(-1, 0), 'color': RED },
			{ 'position': Vector( 1, 0), 'color': RED },
			{ 'position': Vector(-1, 1), 'color': RED },
			{ 'position': Vector( 0, 1), 'color': RED },
			{ 'position': Vector( 1, 1), 'color': RED }
		]
		sprite3 = [
			{ 'position': Vector(-1,-1), 'color': RED },
			{ 'position': Vector( 1, 1), 'color': RED },
			{ 'position': Vector( 1,-1), 'color': RED },
			{ 'position': Vector(-1, 1), 'color': RED }
		]

		Sprite.__init__(self, [ sprite1, sprite2, sprite3 ], self.duration, AnimationLoopType.OneTime)

		self.position = position