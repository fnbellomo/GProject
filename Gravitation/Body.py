#!/usr/bin/env python3

from __future__ import print_function

#import numpy as np
from numpy import sqrt as np_sqrt


class Body(object):
    """
    This class represents a Body
    """

    def __init__(self, obj_id, obj_mass, obj_position, obj_velocity):
        """
        The components of the body are
        """

        self.obj_id      	= obj_id		# id		, can be any format
        self.obj_mass    	= float(obj_mass)	# mass		, float format
        self.obj_position	= obj_position		# position	, list=[float,float] format
        self.obj_velocity	= obj_velocity		# velocities	, list=[float,float] format
        self.obj_path		= [[self.obj_position[0]],[self.obj_position[1]]]	# path 		, list=[pathx,pathy] format

    def step(self, step_func, step_size, bodies_list, dict_bodies):
        """
        Take a step for the position and velocity of the body
        """

        self.obj_position,self.obj_velocity = step_func(step_size,self.obj_id,bodies_list,dict_bodies)
        print(self.obj_id,self.obj_position,self.obj_velocity)
	
    def gfactor(self, other_body):
        """
        This function computes the g_ij factor between this object and other_object
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
