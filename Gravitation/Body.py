#!/usr/bin/env python3 
from __future__ import print_function
from toy_funcs import *

class Body(object):
    """This class represents a Body"""
    def __init__(self, obj_id, obj_mass, obj_position, obj_velocity):
        """The components of the body are"""
	self.obj_id      	= obj_id	# id		, can be any format
	self.obj_mass    	= float(obj_mass)	# mass		, float format
	self.obj_position	= obj_position	# position	, list=[float,float] format
	self.obj_velocity	= obj_velocity	# velocities	, list=[float,float] format
    def step(self, step_func, step_size, bodies_list, dict_bodies):
        """Take a step for the position and velocity of the body"""
        self.obj_position,self.obj_velocity = step_func(step_size,self.obj_id,bodies_list,dict_bodies)
	print(self.obj_id,self.obj_position,self.obj_velocity)
