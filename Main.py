#!/usr/bin/env python3 
from __future__ import print_function
#import sys
#import os
#sys.path.append(os.path.abspath('Gravitation/'))
#from Gravitation import *
from Gravitation.Gravitation import *
import argparse

menu_text1 = """
    1 - Add body
    2 - Take step
    0 - Exit
"""
# Creation of argument parser
parser = argparse.ArgumentParser(description='n-body gravitation')
parser.add_argument('--method', dest='method',default="runge-kutta4",help='integration method. runge-kutta4 or euler')
parser.add_argument('--tstep', dest='tstep',default=1, help='time step')
parser.add_argument('--file', dest='filename',default="bodies.dat", help='body parameters filename')
parser.add_argument('--plot', dest='do_plot',action='store_true',default=False, help='plot the results in real time')
args = parser.parse_args()


def main():
	grav	= Gravitation()
	grav.import_bodies(args.filename)
	grav.setUpInt(args.method, args.tstep, args.do_plot)
	plot = make_plot(grav)

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
#			grav.print_status(True)
			grav.take_steps(number_of_steps,plot,True)
	        elif selected_option == 0:
			exit(0)
if __name__ == '__main__':
    main()
