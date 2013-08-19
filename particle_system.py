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
	def __init__(self, viscosity=0, gravity=0):
		self.particle_generator = ParticleGenerator()
		self.attractors = Particles()
		self.viscosity=viscosity
		self.gravity=gravity
		
	def update(self, toric):
		self.particle_generator.update()
		temp=PVector()
		for i in self.particle_generator.particles.particle_list:
			drag=i.velocity*i.size*i.size*self.viscosity*-1
			i.apply_force(PVector(0, self.gravity))
			for j in self.attractors.particle_list:
				j.apply(i)	
					
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
	def __init__(self, canvas, gravity=0, toric=FALSE):
		self.particle_systems=list()
		self.canvas=canvas
		screen=canvas
		self.toric=toric

	def add_particle_system(self, ps):
		self.particle_systems.append(ps)
		
	def update(self):
		for i in self.particle_systems:
			i.update(self.toric)
			
	def plot(self):
		for i in self.particle_systems:
			i.plot(self.canvas, self.toric)
	
