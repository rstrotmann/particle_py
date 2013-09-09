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

	
fl=Flame(320, 320, size=30, n=15, divergence=.5, lifespan=80)
fl1=Flame(300, 280, size=20, n=15, divergence=.5, lifespan=80)
	
w=World(frame, toric=FALSE)

ps_fl=ParticleSystem(gravitation=FALSE)
ps_fl.particle_generator=fl

ps_fl1=ParticleSystem(gravitation=FALSE)
ps_fl1.particle_generator=fl1

w.add_particle_system(ps_fl)
#w.add_particle_system(ps_fl1)

frame.bind("<Button-1>", click)
frame.pack()

while 1==1:
	frame.delete(ALL)
	w.update()
	w.plot()
	frame.update()
	
root.mainloop()





















