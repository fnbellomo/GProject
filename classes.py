#!/usr/bin/env python3 
from __future__ import print_function
from toy_funcs import *
#import pylab as plt

import matplotlib
#To make interactive plots, I need use TK
matplotlib.use('TkAgg')
#Matplotlib configuration parameters:
matplotlib.rcParams.update({'font.size': 18, 'text.usetex': True})

import matplotlib.pyplot as plt

#To make the same body have the same color
import matplotlib.colors as colors
import matplotlib.cm as cmx

class make_plot():
    """
    Class to make the plots in run time
    """

    def __init__(self, body_numbers):
        self.body_numbers = body_numbers
        #Turn interactive mode on.
        plt.ion()
        #Creo que no es necesario el show
        plt.show()

        #Setup the plot
        self.fig, self.axes = plt.subplots(figsize=(12,3))

        #Set x, y label and title
        self.axes.set_xlabel(r'$x$')
        self.axes.set_ylabel(r'$y$')
        self.axes.set_title('Solution of %s body problems' %(self.body_numbers))

        #To make that the same body have the same color
        body_range = range(self.body_numbers)
        curves = [np.random.random(20) for i in body_range]
        jet = cm = plt.get_cmap('jet') 
        cNorm  = colors.Normalize(vmin=0, vmax=body_range[-1])
        self.scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    #Update the plots
    def update(self, x, y):
        #x and y are position vectors for all bodys
        for i in range(self.body_numbers):
            colorVal = self.scalarMap.to_rgba(i)
            self.axes.plot(x[i], y[i], 'o', color=colorVal)
        plt.draw()


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

