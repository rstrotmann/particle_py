#!/usr/bin/python

from Tkinter import *
import math
import time
import threading
import random

gravity = 0.001


class PVector:
	def __init__ (self, x=0, y=0):
		self.x=x
		self.y=y
	
# 	def get_x(self):
# 		return self.x
# 		
# 	def set_x(self, x):
# 		self.x = x
# 		
# 	def set_y(self, y):
# 		self.y = y
# 		
# 	def get_y(self):
# 		return self.y
# 	
# 	x=property(get_x, set_x)
# 	y=property(get_y, set_y)
	
	def dump(self):
		print self.x, self.y

	def __add__(self, other):
		return PVector(self.x+other.x, self.y+other.y)
		
	def __sub__(self, other):
		return PVector(self.x-other.x, self.y-other.y)
	
	def __mul__(self, n):
		return PVector(float(self.x)*n, float(self.y)*n)
		
	def __div__(self, n):
		return PVector(float(self.x)/n, float(self.y)/n)

	def __abs__(self):
		return math.sqrt(self.x*self.x+self.y*self.y)
		
	def normal(self):
		if(abs(self)!=0):
			return PVector(self.x/abs(self), self.y/abs(self))
		else:
			return self

		

class Particle:
	def __init__(self, x=0, y=0, x_vel=0, y_vel=0, x_accel=0, y_accel=0, color="black",
		lifespan=100, size=8, jitter=0, density=1):
		self.position=PVector(x,y)
		self.velocity=PVector(x_vel, y_vel)
		self.max_velocity=10
		self.acceleration=PVector(x_accel, y_accel)
		self.color=color
		self.lifespan=lifespan
		self.life=lifespan
		self.size=size
		self.jitter=jitter
		self.density=density
		
# 	def get_position(self):
# 		return self.position
# 		
# 	def get_velocity(self):
# 		return self.velocity
# 	
# 	def get_acceleration(self):
# 		return self.acceleration
# 		
# 	def set_position(self, position):
# 		self.position=position
# 		
# 	def set_velocity(self, velocity):
# 		self.velocity=velocity
# 		
# 	def set_acceleration(self, acceleration):
# 		self.acceleration=acceleration
# 	
# 	def set_size(self, size):
# 		self.size = float(size)
# 		
# 	def get_size(self):
# 		return float(size)
# 	
	def get_age(self):
		return self.life/float(self.lifespan)
# 		
# 	def set_age(self, age):
# 		self.life = age*self.lifespan
# 		
# 	def get_color(self):
# 		return self.color
# 	
# 	def set_color(self, color):
# 		self.color=color
# 		
# 	position=property(get_position, set_position)
# 	velocity=property(get_velocity, set_velocity)
# 	acceleration=property(get_acceleration, set_acceleration)
# 	size = property(get_size, set_size)
 	age = property(get_age)
# 	color = property(get_color, set_color)
	
	def accelerate(self, acc):
		self.acceleration += acc
		
	def plot(self, c, toric=FALSE, color="black"):
		c.create_oval(self.position.x-self.size/2, self.position.y-self.size/2,
			self.position.x+self.size/2, self.position.y+self.size/2,
			outline=self.color, fill=self.color)
			
	def apply_force(self, force):
		self.acceleration += force/self.size*self.density
		
	def dump(self):
		print self.position.x, self.position.y
		
	def isDead(self):
		if(self.life<0):
			return TRUE
		else:
			return FALSE
	
	def contains_x(self, x):
		if((x >= self.position.x-self.size/2) & (x <= self.position.x+self.size/2)):
			return TRUE
		else:
			return FALSE

	def update(self):
		self.acceleration+=PVector((random.random()-.5)*self.jitter, (random.random()-.5)*self.jitter)
		self.velocity += self.acceleration
		if(self.velocity > self.max_velocity):
			self.velocity = self.max_velocity
		self.position = self.position + self.velocity
		self.life -=1
		self.acceleration=PVector(0,0)


class Particles:
	def __init__(self):
		self.particle_list = list()
		self.index=0
		
	def __add__(self, x=PVector(0,0)):
		self.particle_list.append(x)
		
	def add(self, x = PVector(0,0)):
		self.particle_list.append(x)
	
	def dump(self):
		for i in self.particle_list:
			i.dump()
	
	def plot(self, c, toric):
		for i in self.particle_list:
			i.plot(c, toric)

	def clear(self, c):
		c.delete(ALL)
							
	def update(self):
		for i in self.particle_list:
			i.update()
			if(i.isDead()):
				self.particle_list.remove(i)
				
	def count(self):
		return len(self.particle_list)