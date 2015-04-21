#!/usr/bin/env python3 
from __future__ import print_function
from Body import Body
from Plot import make_plot
#from toy_funcs import *
import numpy as np
from RK import *

def float_list(LIST): return [float(l) for l in LIST]
best_mass	= 1
best_distance	= 1
best_time	= 1
# distance : 1.5E+11 m (averange distance beetween Earth to sun)
# mass : 5.9736E+24 kg (Earth mass)
# time: 3.1104E07: 
best_mass	= 1.5E+11
best_distance	= 5.9736E+24 
best_time	= 3.1104E07
class Gravitation(object):
    """
    This class is the main Gravitaion wrapper
    """
    def __init__(self,scale_mass=best_mass,scale_distance=best_distance,scale_time=best_time):
        """ Compose a list and a dict with all bodies 
		.bodies  corresponds to a list with the bodies, i. e. [Body1,Body2,...]		=> GRAV.bodies[1]   = Body1 
		.lookup  corresponds to a dict with the bodies, i. e. dict([id1,Body1],...)	=> GRAV.lookup[id1] = Body1
	"""
        self.bodies	= []
        self.lookup	= dict([[body.obj_id,body] for body in self.bodies])
	self.convert_m	= scale_mass	/ best_mass	
	self.convert_r	= scale_distance/ best_distance
	self.convert_t	= scale_time	/ best_time	
	self.convert_v	= self.convert_r/ self.convert_t	
	self.step_size	= 0.1
    def add_body(self, obj_id, obj_mass, obj_position, obj_velocity):
        """ Add a body to the list with all bodies """
	# All dimensions are scaled
	mass		= float(obj_mass)*self.convert_m
	position	= [pos*self.convert_r for pos in obj_position]	
	velocity	= [vel*self.convert_v for vel in obj_velocity]	
	new_Body	= Body(obj_id,mass,position,velocity)

	self.bodies.append( new_Body )
	self.lookup[obj_id] = new_Body
	print('*** Body = ',obj_id, obj_mass, obj_position, obj_velocity,' added ***',sep='\t')
    def import_bodies(self, filename):
        """ Reads bodies from a file """
	file_in	= open(filename,'r')
	lines	= file_in.readlines ()
	file_in.close ()
	for i in range(1,len(lines)):
		if lines[i] != "\n" :
			aux = lines[i].split ()
			self.add_body(aux[0],aux[1],float_list(aux[2:4]),float_list(aux[4:6]))
#			self.add_body(obj_id, obj_mass, obj_position, obj_velocity)

    def take_steps(self, number_of_steps,plot):
        """ Takes steps for all bodies """
	for i in range(number_of_steps):
		print('\nstep =',i)
		moveRK4(self.step_size,self.bodies)
#		for body in self.bodies:
#			body.step(step_func, self.step_size, self.bodies, self.lookup)
		self.print_status(plot)
    def print_status(self,plot):
        """ Print the position for all bodies """
#	print_func(self.bodies,first_step)
	plot.update()
#        try:
#                acc.withdraw(amount)
#        except NotEnoughFundsException:
#                print("Dear client, you should check your balance before performing this operation")

