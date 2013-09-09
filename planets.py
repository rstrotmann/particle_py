#!/usr/bin/python

from Tkinter import *
import math
import time
import threading
import random

from particle import *
from particle_generator import *
from particle_system import *


screen_width = 640
screen_height = 360


root = Tk()
frame = Canvas(root, width=screen_width, height=screen_height, background="white")
frame.grid(row=0, column=0)

def click(event):
	sd.spawn()
	
sd = Cannon (340, 50, 3, 0, 0, 0, color="red", size=20, n=1, divergence=0.5,
	lifespan=100000, density=0)	

	
w=World(frame, toric=FALSE)
p=ParticleSystem(gravitation=TRUE, viscosity=0)
p.particle_generator=sd

c=Attractor (300, 150, 1,0,0,0, size=50, force=20)
p.attractors.add(c)

w.add_particle_system(p)

#frame.bind("<Button-1>", click)
frame.bind_all("<Key>", click)
frame.pack()

while 1==1:
	frame.delete(ALL)
	w.update()
	w.plot()
	frame.update()
	
root.mainloop()





















