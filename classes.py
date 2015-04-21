#!/usr/bin/env python3 
from __future__ import print_function
from toy_funcs import *
#import pylab as plt

class NotEnoughFundsException(Exception):
    def __init__(self, message):
        self.value = message  

class Body(object):
    """This class represents a Body"""
    def __init__(self, obj_id, obj_mass, obj_position, obj_velocity):
        """The components of the body are"""
	self.obj_id      	= obj_id	# id		, can be any format
	self.obj_mass    	= obj_mass	# mass		, float format
	self.obj_position	= obj_position	# position	, list=[float,float] format
	self.obj_velocity	= obj_velocity	# velocities	, list=[float,float] format
    def step(self, step_func, step_size, bodies_list, dict_bodies):
        """Take a step for the position and velocity of the body"""
        self.obj_position,self.obj_velocity = step_func(step_size,self.obj_id,bodies_list,dict_bodies)
	print(self.obj_id,self.obj_position,self.obj_velocity)

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

menu_text1 = """
    1 - Add body
    2 - Take step
    0 - Exit
"""

def main():
	grav	= Gravitation()

	while True:
	        print(menu_text1)
	        selected_option = int(input("Option: "))
	        print()
	        
	        if selected_option == 1:
			obj_id		= (input('obj_id:	'))
			obj_mass	= (input('obj_mass:	'))
			obj_position	= (input('obj_position:	'))
			obj_velocity	= (input('obj_velocity:	'))
			grav.add_body(obj_id, obj_mass, obj_position, obj_velocity)
			
	        elif selected_option == 2:
			number_of_steps	= (input('number_of_steps:	'))
			grav.take_steps(number_of_steps, step_func)
	        elif selected_option == 0:
			exit(0)
if __name__ == '__main__':
    main()

