# -*- coding: utf8 -*- 

#http://wpf-animation.googlecode.com/svn/trunk/src/WPF/Animation/PennerDoubleAnimation.cs
#https://github.com/danro/jquery-easing/blob/master/jquery.easing.js
class AnimationAlgorithm:
	# no easing, no acceleration
	@staticmethod
	def Linear(t, c, b, d): return t
	# accelerating from zero velocity
	@staticmethod
	def EaseInQuad(t, c, b, d): return t*t
	# decelerating to zero velocity
	@staticmethod
	def EaseOutQuad(t, c, b, d): return t*(2-t) 
	# acceleration until halfway, then deceleration
	@staticmethod
	def EaseInOutQuad(t, c, b, d): return 2*t*t if t<.5 else -1+(4-2*t)*t 
	# accelerating from zero velocity 
	@staticmethod
	def EaseInCubic(t, c, b, d): return t*t*t 
	# decelerating to zero velocity !!! BROKEN !!!
	@staticmethod
	def EaseOutCubic(t, c, b, d): return (--t)*t*t+1 
	# acceleration until halfway, then deceleration 
	@staticmethod
	def EaseInOutCubic(t, c, b, d): return 4*t*t*t if t<.5 else (t-1)*(2*t-2)*(2*t-2)+1 
	# accelerating from zero velocity 
	@staticmethod
	def EaseInQuart(t, c, b, d): return t*t*t*t 
	# decelerating to zero velocity 
	@staticmethod
	def EaseOutQuart(t, c, b, d): return 1-(--t)*t*t*t 
	# acceleration until halfway, then deceleration
	@staticmethod
	def EaseInOutQuart(t, c, b, d): return 8*t*t*t*t if t<.5 else 1-8*(--t)*t*t*t 
	# accelerating from zero velocity
	@staticmethod
	def EaseInQuint(t, c, b, d): return t*t*t*t*t 
	# decelerating to zero velocity !!! BROKEN !!!
	@staticmethod
	def EaseOutQuint(t, c, b, d): return 1+(--t)*t*t*t*t 
	# acceleration until halfway, then deceleration 
	@staticmethod
	def EaseInOutQuint(t, c, b, d): return 16*t*t*t*t*t if t<.5 else 1+16*(--t)*t*t*t*t
	# 
	@staticmethod
	def EaseOutElastic(t, c, b, d):
		ts = (t/d)*t
		tc = ts*t
		return b+c*(-8.1525*tc*ts + 28.5075*ts*ts + -35.105*tc + 16*ts + -0.25*t)
	# 
	@staticmethod
	def EaseInElastic(t, c, b, d):
		s = 1.70158; 
		if (t/d/2) < 1: return c/2*(t*t*(((s * (1.525))+1) * t - s)) + b
		else: return c/2*((t-2)*t*(((s*(1.525))+1)*t + s) + 2) + b
	# exponentially decaying parabolic bounce
	@staticmethod
	def EaseOutBounce(t, c, b, d):
		if ( t / d ) < ( 1 / 2.75 ):
			return c * ( 7.5625 * t * t ) + b
		elif t < ( 2 / 2.75 ):
			return c * ( 7.5625 * ( t - ( 1.5 / 2.75 ) ) * t + .75 ) + b
		elif t < ( 2.5 / 2.75 ):
			return c * ( 7.5625 * ( t - ( 2.25 / 2.75 ) ) * t + .9375 ) + b
		else:
			return c * ( 7.5625 * ( t - ( 2.625 / 2.75 ) ) * t + .984375 ) + b
	#deceleration until halfway, then acceleration.
	@staticmethod
	def EaseInBounce(t, b, c, d):
		return c - AnimationAlgorithm.EaseOutBounce(d-t, 0, c, d) + b

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
		if self.duration <= 0:
			self.currentValue = 0
			return

		if self.direction == AnimationDirection.Forward:
			self.time += dt
		else:
			self.time -= dt

		if self.time > self.endTime or self.time < 0:
			if self.loop == AnimationLoopType.Loop:
				self.startTime = self.time
				self.endTime = self.startTime + self.duration
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

		t = (self.time - self.startTime) / self.duration
		self.currentValue = self.algorithm(t, self.time, self.startTime, self.duration)
	
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
