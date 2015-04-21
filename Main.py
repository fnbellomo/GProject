#!/usr/bin/env python3 
from __future__ import print_function
from Gravitation import Gravitation
from Plot import make_plot

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

