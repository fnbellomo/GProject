#!/usr/bin/env python3

from __future__ import print_function

from Gravitation.Gravitation import *

#To parse the argument from comand line
import argparse

# Profiling options
import cProfile, pstats, StringIO

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
parser.add_argument('--profile', dest='profile',action='store_true',default=False, help='runs without interaction mode - only for profiling')
parser.add_argument('--nsteps', dest='nsteps',default=0, help='total number of time steps')
parser.add_argument('--config', dest='use_config',action='store_true',default=False, help='uses a configuration file')
parser.add_argument('--confile', dest='config_file',default='config.py', help='passes a configuration file')
args = parser.parse_args()


def main():
	if args.profile == False:
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
			number_of_steps = (input('number_of_steps: '))
			plot_every_n = 1
			if grav.do_plot == True :
				plot_every_n = (input('plot each n steps?\n'))
			grav.take_steps(number_of_steps,plot,plot_every_n)
			print_in_file = str(raw_input('Save plot (y/n):\n '))
			if print_in_file == 'y':
				if grav.do_plot == False :
					plot_every_n = (input('plot each n steps?\n'))
				grav.save_plot(number_of_steps,plot,plot_every_n)
		elif selected_option == 0:
			exit(0)

	else:
		# Enable profiling with cProfile
		pr = cProfile.Profile()
		pr.enable()

		grav = Gravitation()
		grav.import_bodies(args.filename)
		grav.setUpInt(args.method, args.tstep, args.do_plot)
		grav.take_steps_np(int(args.nsteps))

		pr.disable()
		pr.print_stats()

if args.use_config == False:	        
	if __name__ == '__main__':
	    main()
else:
	from config import *
	grav	= Gravitation()
	grav.import_bodies(filename)
	grav.setUpInt(method, tstep,do_plot)
	plot = make_plot(grav)

	grav.take_steps(number_of_steps,plot,plot_every_n)
	if save_plot == True:
		grav.save_plot(number_of_steps,plot,plot_every_n)
