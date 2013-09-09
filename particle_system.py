#!/usr/bin/python

from Tkinter import *
import math
import time
import threading
import random
from particle import *
from particle_generator import *


screen_width = 600
screen_height = 600



class ParticleSystem:
	def __init__(self, viscosity=0, gravitation=TRUE):
		self.particle_generator = ParticleGenerator()
		self.attractors = Particles()
		self.viscosity=viscosity
		self.gravitation=gravitation
		
	def update(self, toric):
		self.particle_generator.update()
		temp=PVector()
		for i in self.particle_generator.particles.particle_list:
			drag=i.velocity*i.size*i.size*self.viscosity*-1
			i.apply_force(drag)	
			i.apply_force(PVector((random.random()-0.5)*i.jitter, (random.random()-0.5)*i.jitter))	
			if self.gravitation==TRUE:
				for j in self.particle_generator.particles.particle_list:
					dir=(j.position-i.position)
					distance=abs(dir)
					if distance!=0:
						m=i.size*j.size*i.density*j.density/distance/distance
						if(m>1):
							m=1
						i.apply_force(dir.normal()*m)
			for j in self.attractors.particle_list:
				dir=(j.position-i.position)
				distance=float(abs(dir))	
				m=j.size*i.size*i.density*j.force/distance/distance
				if(m>1):
					m=1
				i.apply_force(dir.normal()*m)
							

					
	def plot(self, c, toric):
		self.particle_generator.plot(c)
		for a in self.attractors.particle_list:
			a.plot(c, toric)
	


class ParticleSystems:
	def __init__(self):
		self.particle_systems = list()
		self.index=0
		
	def __add__(self, x=PVector(0,0)):
		self.particle_systems.append(x)
		
	def add(self, x = PVector(0,0)):
		self.particle_systems.append(x)
	
	def dump(self):
		for i in self.particle_list:
			i.dump()
	
	def plot(self, c, toric):
		for i in self.particle_systems:
			i.plot(c, toric)

	def clear(self, c):
		c.delete(ALL)
							
	def update(self):
		for i in self.particle_systems:
			i.update()
				
	def count(self):
		return len(self.particle_systems)




class World:
	def __init__(self, canvas, width=300, height=300, gravitation=0, toric=FALSE):
		self.particle_systems=list()
		self.canvas=canvas
		screen=canvas
		self.toric=toric

	def add_particle_system(self, ps):
		self.particle_systems.append(ps)
		
	def update(self):
		for i in self.particle_systems:
			i.update(self.toric)
			if self.toric==TRUE:
				for j in i.particle_generator.particles.particle_list:
					if j.position.x >= float(self.canvas.cget("width")):
						j.position = PVector(0, j.position.y)
					if j.position.x < 0:
						j.position.x = float(self.canvas.cget("width"))
					if j.position.y >= float(self.canvas.cget("height")):
						j.position = PVector(0, j.position.y)
					if j.position.y < 0:
						j.position.y = float(self.canvas.cget("height"))									
			
	def plot(self):
		for i in self.particle_systems:
			i.plot(self.canvas, self.toric)
	

class Box (World):
	def __init__ (self, canvas, gravitation=0.01, width=300, height=300):
		World.__init__(self, canvas, gravitation)
		self.width=width
		self.height=height
	
	def update(self):
		World.update(self)
		for i in self.particle_systems:
			for j in i.particle_generator.particles.particle_list:
				j.apply_force(PVector(0,0.5*j.size*j.density))
				if j.position.y+j.size/2 > self.height:
					j.position.y=self.height-j.size/2
					j.velocity.y=j.velocity.y*-0.85
					j.velocity.x=j.velocity.x*.9
				if j.position.x+j.size/2 > self.width:
					j.position.x=self.width-j.size/2
					j.velocity.x = j.velocity.x*-.85
					j.velocity.y = j.velocity.y*.9	
				if j.position.x-j.size/2 < 0:
					j.position.x = 0+j.size/2
					j.velocity.x *= -0.85
					j.velocity.y *= 0.9
					
		