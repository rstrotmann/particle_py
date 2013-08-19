#!/usr/bin/python

from Tkinter import *
import math
import time
import threading
import random

from particle import *
from particle_generator import *
from particle_system import *


screen_width = 600
screen_height = 600


root = Tk()
frame = Canvas(root, width=screen_width, height=screen_height, background="white")
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
	


def click(event):
	sd.spawn()

	
sd = Cannon (300, 200, -3, 2, 0, 0, color="red", size=20, n=1, divergence=0.3,
	lifespan=100000)	

w=World(frame)
p=ParticleSystem(gravity=0, viscosity=0)
p.particle_generator=sd
a=Attractor (200, 450, 0,0,0,0, size=50, force=20)
b=Attractor (100, 300, 0,0,0,0, size=20, force=20)
c=Attractor (300, 300, 1,0,0,0, size=50, force=20)
d=Attractor (400, 200, 0,0,0,0, size=20, force=20)
e=Attractor (400, 150, 0,0,0,0, size=20, force=20)

p.attractors.add(a)
p.attractors.add(b)
p.attractors.add(c)
p.attractors.add(d)
p.attractors.add(e)

w.add_particle_system(p)

frame.bind("<Button-1>", click)
frame.pack()

while 1==1:
	frame.delete(ALL)
	w.update()
	w.plot()
	frame.update()
	
root.mainloop()





















