#!/usr/bin/env python3

from __future__ import print_function

#import numpy as np
from numpy import sqrt as np_sqrt


class Body(object):
    """
    Base class for space bodies

    Parameters
    ----------
    body : spatial object

    This class is responsible for creating objects that would be attracted in the same Gravitational object.
    The class contains specific information such as position, velocity and mass.
    """

    def __init__(self, obj_id, obj_mass, obj_position, obj_velocity):
        """
        Class startup
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
        Computes the g_ij factor between this object and other_body

        g_ij = G * mj / d**3 

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

    def position_array(self):
        """
        Retorna 1 lista con 4 arrays. Dos de las posiciones en x e y de todos los cuerpos. Los otros dos son los path en x e y de cada cuerpo.
        """
        x = []
        y = []
        xp = []
        yp = []
        for body in self.bodies:
            x.append(self.obj_position[0])
            y.append(self.obj_position[1])
            xp.append(self.obj_path[0])
            yp.append(self.obj_path[1])

        return([x, y, xp, yp])
