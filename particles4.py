#!/usr/bin/python

from Tkinter import *
import math
import time
import threading
import random
from particle import *
screen_width = 600
screen_height = 600

from particle import *
from particle_generator import *
#gravity = PVector(0,0.001)

root = Tk()
frame = Canvas(root, width=screen_width, height=screen_height, background="white")
#frame.grid(row=0, column=0)
#frame = Frame(root, width=screen_width, height=screen_height, background="white")
#frame = Canvas(window, width=screen_width, height=screen_height, background="white")
frame.grid(row=0, column=0)

class Attractor(Particle):
	def __init__(self, x=0, y=0, x_vel=0, y_vel=0, x_accel=0, y_accel=0, color="black",
		lifespan=100, size=8, jitter=0, force=0):
		self.position=PVector(x,y)
		self.velocity=PVector(x_vel, y_vel)
		self.max_velocity=10
		self.acceleration=PVector(x_accel, y_accel)
		self.color=color
		self.lifespan=lifespan
		self.life=lifespan
		self.size=size
		self.jitter=jitter
		self.force=force
		
	def isDead(self):
		return FALSE
				
	def apply(self, p):
		dir=(self.position-p.position)
		distance=abs(dir)
		m=self.force*self.size*p.size/distance/distance
		if(m>1):
			m=1
		#frame.create_line(self.position.x, self.position.y,
		#	self.position.x+dir.normal().x*m*1000, self.position.y+dir.normal().y*m*1000)
		p.apply_force(dir.normal()*m)
		
	def get_force(self, p):
		dir=(self.position-p.position)
		distance=abs(dir)
		m=self.force*self.size*p.size/distance/distance
		if(m>.1):
			m=.1
		return dir.normal()*m
	
	def plot(self, c, color="black"):
		c.create_oval(self.position.x-self.size/2, self.position.y-self.size/2,
			self.position.x+self.size/2, self.position.y+self.size/2,
			outline=self.color)
	


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
			#for a in self.attractors.particle_list:
			#	a.apply()
				#temp += a.get_force(i)
			#i.accelerate(temp/self.attractors.count())
			#i.accelerate(temp)
		#self.particleGenerator.update()
			drag=i.velocity*i.size*i.size*self.viscosity*-1
			#i.apply_force(drag)
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
		#self.gravity=PVector(0, gravity)
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
	



def click(event):
	sd.spawn()

		

	
fl = Flame(300, 250, dir_x=5, dir_y=.2, divergence=.6, n=100, color="red", size=20,
	lifespan=80)
fl1 = Flame(200, 250, dir_x=5, dir_y=.2, divergence=.6, n=100, color="red", lifespan=70)

#sd = Seeder(300, 300, 0, 0, 0, 0, color="red", size=10, n=1, divergence=600,
#	lifespan=200000, jitter=0)

sd = Cannon (300, 200, 2, -.02, 0, 0, color="red", size=20, n=1, divergence=.3,
	lifespan=100000)

sd = Cannon (300, 200, 2, -.02, 0, 0, color="red", size=20, n=10, divergence=0,
	lifespan=100000)	

w=World(frame)
p=ParticleSystem(gravity=0, viscosity=0)
p.particle_generator=sd
a=Attractor (200, 450, 0,0,0,0, size=20, force=20)
b=Attractor (100, 300, 0,0,0,0, size=20, force=20)
c=Attractor (300, 300, 1,0,0,0, size=50, force=20)
d=Attractor (400, 200, 0,0,0,0, size=20, force=20)
p.attractors.add(a)
p.attractors.add(b)
p.attractors.add(c)
p.attractors.add(d)
w.add_particle_system(p)

#sd=Cannon(100,100,2,0, divergence=0.8)
#sd = Flame(300, 250, dir_y=-4, n=100, divergence=.95, size=20, jitter=0.01, lifespan=70)
#a = Attractor (350, 150, 0,0,0,0, size=50, force=.02)
#b = Attractor (200, 150, 0,0,0,0, size=50, force=.01)

#ps=ParticleSystem(viscosity=.0001)
#ps.set_particle_generator(sd)
#ps.add_attractor(a)
#ps.add_attractor(b)

#r=Rain(0,0,0,50, n=100, size=4, )
#rp=Attractor(200, 250, size=50, force=2)
#rs=ParticleSystem()
#rs.set_particle_generator(r)
#rs.add_attractor(rp)


frame.bind("<Button-1>", click)
frame.pack()
#frame.focus_set()


#for i in range(1,10000):
while 1==1:
	frame.delete(ALL)

	w.update()
	w.plot()
	
	#ps.update()
	#rs.update()
	
	#ps.plot(frame)
	#rs.plot(frame)

	frame.update()
	#frame.after(5)
	
root.mainloop()





















