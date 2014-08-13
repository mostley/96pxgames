# -*- coding: utf8 -*- 

class AnimationAlgorithm:
	@staticmethod
	def Linear(time, startTime, duration):
		return (time - startTime) / duration

class AnimationLoopType:
	OneTime = 0
	Loop = 1
	PingPong = 2

class AnimationDirection:
	Forward = 0
	Backward = 1

class Animation:
	def __init__(self, startValue, endValue, duration, loop=AnimationLoopType.Loop, algorithm=AnimationAlgorithm.Linear):
		self.algorithm = algorithm
		self.startValue = startValue
		self.endValue = endValue
		self.duration = duration
		self.loop = loop
		self.ended = False

		self.currentValue = self.startValue

		if isinstance(self.startValue, list) or isinstance(self.startValue, tuple):
			self.currentValue = 0.0

		self.time = 0
		self.startTime = self.time
		self.endTime = self.time + self.duration
		self.direction = AnimationDirection.Forward

	def update(self, dt):
		if self.direction == AnimationDirection.Forward:
			self.time += dt
		else:
			self.time -= dt

		if self.time > self.endTime or self.time < 0:
			if self.loop == AnimationLoopType.Loop:
				self.startTime = self.time
			elif self.loop == AnimationLoopType.PingPong:
				if self.direction == AnimationDirection.Forward:
					self.direction = AnimationDirection.Backward
					self.time = self.endTime
				else:
					self.direction = AnimationDirection.Forward
					self.time = 0
			else:
				self.ended = True
				self.time = self.endTime

		self.currentValue = self.algorithm(self.time, self.startTime, self.duration)
	
	def restart(self):
		self.time = 0
		self.direction = AnimationDirection.Forward

	def getValue(self):
		if isinstance(self.startValue, list) or isinstance(self.startValue, tuple):
			result = []
			for i in range(len(self.startValue)):
				result.append( self.startValue[i] + ( (self.endValue[i] - self.startValue[i]) * self.currentValue ) )
			return result
		else:
			return self.startValue + ( (self.endValue - self.startValue) * self.currentValue )
