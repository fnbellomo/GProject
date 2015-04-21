#!/usr/bin/env python3 
from __future__ import print_function
from Body import Body
from toy_funcs import *

class Gravitation(object):
    """
    This class is the main Gravitaion wrapper
    """
    def __init__(self):
        """ Compose a list with all bodies """
#        self.bodies	= []
        self.bodies	= [Body(1,1,[0,0],[2,-3])]
        self.lookup	= dict([[body.obj_id,body] for body in self.bodies])
	self.step_size	= 0.1
    def add_body(self, obj_id, obj_mass, obj_position, obj_velocity):
        """ Add a body to the list with all bodies """
	new_Body	= Body(obj_id, obj_mass, obj_position, obj_velocity)
	self.bodies.append( new_Body )
	self.lookup[obj_id] = new_Body

    def take_steps(self, number_of_steps, step_func):
        """ Takes steps for all bodies """
	for i in range(number_of_steps):
		for body in self.bodies:
			body.step(step_func, self.step_size, self.bodies, self.lookup)
		self.print_status()
    def print_status(self):
        """ Print the position for all bodies """
	print_func(self.bodies)
#        try:
#                acc.withdraw(amount)
#        except NotEnoughFundsException:
#                print("Dear client, you should check your balance before performing this operation")
