#!/usr/bin/env python3 
from __future__ import print_function
from Gravitation import *

menu_text1 = """
    1 - Add body
    2 - Take step
    0 - Exit
"""
def main():
	grav	= Gravitation()
	grav.import_bodies('test_bodies.dat')

	while True:
	        print(menu_text1)
	        selected_option = int(input("Option: "))
	        print()
	        
	        if selected_option == 1:
			obj_id		= (raw_input('obj_id	(can be any format):\n'))
			obj_mass	= (input('obj_mass	(float format):\n'))
			obj_position	= (input('obj_position	(list=[float,float] format):\n'))
			obj_velocity	= (input('obj_velocity	(list=[float,float] format):\n'))
			grav.add_body(obj_id, obj_mass, obj_position, obj_velocity)
			
	        elif selected_option == 2:
			number_of_steps	= (input('number_of_steps:	'))
			grav.print_status(True)
			grav.take_steps(number_of_steps, step_func)
	        elif selected_option == 0:
			exit(0)
if __name__ == '__main__':
    main()

