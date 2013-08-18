#!/usr/bin/python

from Tkinter import *
import math
import time
import threading
import random

from particle import *

screen_width = 600
screen_height = 600
gravity = 0.001

class ParticleGenerator:
	def __init__(self, x=0, y=0, dir_x=1, dir_y=1, acc_x=0, acc_y=0, divergence=.4, color="black", n=30,
		size=10, lifespan=800, jitter=0):
		self.position=PVector(x, y)
		self.direction=PVector(dir_x, dir_y)
		self.particles = Particles()
		self.divergence = divergence
		self.n=n
		self.color=color
		self.size=size
		self.lifespan=lifespan
		self.acc_x=acc_x
		self.acc_y=acc_y
		self.jitter=jitter
		self.spawn()	
			
	def spawn(self):
		self.particles.add(Particle(self.position.x, self.position.y,
			self.direction.x * ((1-self.divergence/2) + random.random() * self.divergence),
			self.direction.y * ((1-self.divergence/2) + random.random() * self.divergence),
			y_accel=self.acc_y, x_accel=self.acc_x, color=self.color,
			lifespan=self.lifespan * random.random(), size=self.size, jitter=self.jitter,
			density=0))
	
	def clear(self,c):
		self.particles.clear(c)
	
	def plot(self, c, toric=FALSE):
		self.particles.plot(c, toric)
		
	def update(self):
		self.particles.update()
		if(self.particles.count()<self.n):
			self.spawn()

# 	def get_particles(self):
# 		return self.particles
# 		
# 	def set_particles(self, particles):
# 		self.particles=particles
# 		
# 	particles=property(get_particles, set_particles)

		


class Flame(ParticleGenerator):
	def __init__(self, x=0, y=0, dir_x=1, dir_y=1, acc_x=0, acc_y=.05, divergence=.4, color="black", n=30,
		size=20, lifespan=80, jitter=0):
		ParticleGenerator.__init__(self, x, y, dir_x, dir_y, acc_x, acc_y, divergence, color, n,
		size, lifespan, jitter)

	def spawn(self):
		x=(random.random()-0.5)*self.divergence
		y=(random.random()-0.5)*self.divergence +(1-self.divergence)*self.direction.y
		d=PVector(x,y)
		#d=d/float(abs(d))*random.random()*.7
		self.particles.add(Particle(self.position.x, self.position.y,
			d.x, d.y, 0, self.acc_y, lifespan=self.lifespan*random.random(), size=self.size,
			jitter=self.jitter))
			
	def update(self):
		ParticleGenerator.update(self)
		for i in self.particles.particle_list:
			i.size=(math.sqrt(i.age)*self.size)
			if(self.density(i.position)!=0):
				temp=1/float(self.density(i.position)) * self.particles.count()*100
				#i.set_velocity(PVector(i.get_velocity().x, -.5*temp)) # perhaps use for color
				i.color=(str('#%02x%02x%02x' % (200+50*(1-i.get_age()), 120+100*(1-i.age), 0+10*(1-i.age))))
			heat=0
			for j in self.particles.particle_list:
				if(j.position.y < i.position.y):
					heat += j.contains_x(i.position.x)
			#i.set_velocity(PVector(i.get_velocity().x, -.1*heat)) 
			#i.set_acceleration(PVector(i.get_acceleration().x, -.007*heat)) 
			i.apply_force(PVector(i.acceleration.x, -.07*heat)) 
			#random accelerations
			#i.accelerate(PVector((random.random()-.5)*self.jitter, (random.random()-.5)*self.jitter))
			i.apply_force(PVector((random.random()-.5)*self.jitter, (random.random()-.5)*self.jitter))

		
	def density(self, p):
		sumd=0
		for i in self.particles.particle_list:
			sumd += abs(p-i.position)	
		return sumd
		
	def x_density(self, p):
		sumd=0
		for i in self.particles.particle_list:
			sumd += (p-i.position).x
		return sumd
		


class Ball(ParticleGenerator):
	def update(self):
		ParticleGenerator.update(self)
		for i in self.particles.particle_list:
			if(i.get_position().y >= 300-i.get_size()/2):
				i.set_position(PVector(i.get_position().x, 300))
				i.set_velocity(PVector(i.get_velocity().x*(.5+random.random()*.5), i.get_velocity().y*-1))
				i.set_velocity(i.get_velocity()*.9)



class Cannon(ParticleGenerator):
	def spawn(self):
		self.particles.add(Particle(self.position.x, self.position.y,
			self.direction.x+(random.random()-0.5)*self.divergence,
			self.direction.y+(random.random()-0.5)*self.divergence, 0, 0,
			color=self.color, size=self.size*(0.3+.7*random.random()), jitter=0,
			lifespan=self.lifespan*random.random()))




class Seeder(ParticleGenerator):
	def spawn(self):
		self.particles.add(Particle(self.position.x+(random.random()-0.5)*self.divergence,
			self.position.y+(random.random()-0.5)*self.divergence, self.direction.x, self.direction.y, 0, 0,
			color=self.color, size=self.size, jitter=self.jitter,
			lifespan=self.lifespan*random.random()))



class Rain(ParticleGenerator):
	def spawn(self):
		self.particles.add(Particle(random.random()*screen_width, 0, 0, 
			self.direction.y*random.random(),
			0, random.random()*gravity, color="blue", size=self.size, lifespan=100))
	
	def update(self):
		self.particles.update()
		for i in self.particles.particle_list:
			if(i.position.y>screen_height-i.size/2):
				i.position=PVector(i.position.x, screen_height-i.size/2)
				
		if(self.particles.count()<self.n):
			self.spawn()
	
	

class Sparkle(ParticleGenerator):
	def spawn(self):
		x=(random.random()-0.5)*self.divergence
		y=random.random()-0.5
		d=PVector(x,y)
		d=d/float(abs(d))*random.random()*6
		self.particles.add(Particle(self.position.x, self.position.y,
			d.x, d.y, d.x/10, d.y/10, lifespan=self.lifespan*random.random(), color=self.color, size=self.size))

	def update(self):
		ParticleGenerator.update(self)
		for i in self.particles.particle_list:
			i.set_size(math.sqrt(i.get_age())*self.size)
	


class Fog(ParticleGenerator):
	def spawn(self):
		xx=self.position.x*(random.random()-0.5)*self.divergence
		yy=self.position.y*(random.random()-0.5)
		p=PVector(xx,yy)
		#self.particles.add(Particle(xx, yy, 0, 0, lifespan=self.lifespan*random.random(), color=self.color,
		#	size=self.size*random.random()))	
		#self.particles.add(Particle(p
	