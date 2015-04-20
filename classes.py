#!/usr/bin/env python3 
from __future__ import print_function

class NotEnoughFundsException(Exception):
    def __init__(self, message):
        self.value = message  

class Body(object):
    """This class represents a Body"""
    def __init__(self, obj_id, obj_mass, obj_position, obj_velocity):
	self.obj_id      	= obj_id
	self.obj_mass    	= obj_mass
	self.obj_position	= obj_position
	self.obj_velocity	= obj_velocity

    def step(self, step_func, step_size, all_bodies, dict_bodies):
        """take a step"""
        self.obj_position,self.obj_velocity = step_func(step_size,self.obj_id,all_bodies,dict_bodies)
	print(self.obj_id,self.obj_position,self.obj_velocity)
class Gravitation(object):
    """
    This class is the main Gravitaion wrapper
    """
    def __init__(self):
#        self.bodies	= []
        self.bodies	= [Body(1,1,[0,0],[2,3])]
        self.lookup	= dict([[body.obj_id,body] for body in self.bodies])
	self.step_size	= 0.1
    def add_body(self, obj_id, obj_mass, obj_position, obj_velocity):
	new_Body	= Body(obj_id, obj_mass, obj_position, obj_velocity)
	self.bodies.append( new_Body )
	self.lookup[obj_id] = new_Body

    def take_steps(self, number_of_steps, step_func):
        """Withdraw (amount) from (account_number)"""
	for i in range(number_of_steps):
		for body in self.bodies:
			body.step(step_func, self.step_size, self.bodies, self.lookup)
#        try:
#                acc.withdraw(amount)
#        except NotEnoughFundsException:
#                print("Dear client, you should check your balance before performing this operation")
def step_func(step_size,obj_id,all_bodies,dict_bodies):
	body	= dict_bodies[obj_id]
	for i in range(2):
		body.obj_position[i] += step_size*body.obj_velocity[i]
	return body.obj_position, body.obj_velocity

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

