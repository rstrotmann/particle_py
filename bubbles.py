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

run=0

root = Tk()
frame = Canvas(root, width=screen_width, height=screen_height, background="white")
frame.grid(row=0, column=0)

def click(event):
	sd.spawn()
	#run=1
	
sd = Bubbler (0, 0, 1, 0, 0, -.1, color="blue", size=30, n=10, divergence=.3,
	lifespan=90, height=screen_height, width=screen_width)	

w=World(frame, width=screen_width, height=screen_height)
p=ParticleSystem(gravitation=FALSE, viscosity=0)
p.particle_generator=sd
w.add_particle_system(p)

frame.bind("<Button-1>", click)
frame.pack()

while TRUE:
	frame.delete(ALL)
	w.update()
	w.plot()
	frame.update()
	
root.mainloop()





















