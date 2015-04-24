#!/usr/bin/env python3

from __future__ import print_function

#import numpy as np
from numpy import sqrt as np_sqrt


class Body(object):
    """
    Base class for space bodies.

    This class is responsible for creating objects that would be attracted in the same Gravitational object.
    The class contains specific information such as position, velocity and mass.
    """

    def __init__(self, obj_id, obj_mass, obj_position, obj_velocity):
        """
        Start a Body objects.

        Parameters
        ----------
        obj_id : str
                Body name.
        obj_mass : str
                Body mass.
        obj_position : array_like
                Position in x and y. [x, y]
        obj_velocity : array_like
                Velocity in x and y. [V_x, V_y]
        """

        self.obj_id      	= obj_id		# id		, can be any format
        self.obj_mass    	= float(obj_mass)	# mass		, float format
        self.obj_position	= obj_position		# position	, list=[float,float] format
        self.obj_velocity	= obj_velocity		# velocities	, list=[float,float] format
        self.obj_path		= [[self.obj_position[0]],[self.obj_position[1]]]	# path 		, list=[pathx,pathy] format

    def step(self, step_func, step_size, bodies_list, dict_bodies):
        """
        Take a step for the position and velocity of the body

        Parameters
        ----------
        step_func : 
                  
        step_size : float
                   Size of the time step.
        bodies_list : list
                   List of the name all bodies.
        dict_bodies : dictionary
                   Property dictionary of all bodies
        """

        self.obj_position,self.obj_velocity = step_func(step_size,self.obj_id,bodies_list,dict_bodies)
        print(self.obj_id,self.obj_position,self.obj_velocity)
	
    def gfactor(self, other_body):
        """
        Computes the g_ij factor between this object and other_body
        g_ij = G * mj / d**3 

        Were G is the gravitational constant, mj is the mass of the other objects and d is the distans.
        
        Parameters
        ---------_
        other_body : Object
                    Another body object.
        """
	    
        # Gravity constant
        G = 0.0374038

        if self.obj_id != other_body.obj_id:
	    
            # Distance beetween objects
            dx = self.obj_position[0] - other_body.obj_position[0]
            dy = self.obj_position[1] - other_body.obj_position[1]
            dist = np_sqrt(dx*dx + dy*dy)
	       
            return G*other_body.obj_mass/(dist*dist*dist)
	        
        else:
            return 0
