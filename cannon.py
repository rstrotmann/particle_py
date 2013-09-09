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
	for i in range(1,10):
		sd.spawn()
	sd.n=15
	
sd = Cannon (0, 0, 9, 0, 0, 0, color="red", size=20, n=0, divergence=3,
	lifespan=1000, density=1)	

w=Box(frame, width=screen_width, height=screen_height)
p=ParticleSystem(gravitation=FALSE, viscosity=0)
p.particle_generator=sd
w.add_particle_system(p)

#frame.bind("<Button-1>", click)
frame.bind_all("<Key>", click)
frame.pack()

while TRUE:
	frame.delete(ALL)
	w.update()
	w.plot()
	frame.update()
	
root.mainloop()





















