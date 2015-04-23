#!/usr/bin/env python3 
from __future__ import print_function
import numpy as np
import matplotlib
#To make interactive plots, I need use TK
matplotlib.use('TkAgg')
#Matplotlib configuration parameters:
#matplotlib.rcParams.update({'font.size': 18, 'text.usetex': True})

import matplotlib.pyplot as plt

#To make the same body have the same color
import matplotlib.colors as colors
import matplotlib.cm as cmx

class make_plot(object):
    """
    Class to make the plots in run time
    """

    def __init__(self, grav):
        self.grav = grav
        self.number_body = len(self.grav.bodies)
        self.bodies_range = range(self.number_body)
        self.mass = [grav.bodies[i].obj_mass for i in range(len(grav.bodies))]
        self.mass_max = max(self.mass)
        self.circle_radio = [ m/self.mass_max for m in self.mass]
        
	if grav.do_plot == True:
	        #Turn interactive mode on.
	        plt.ion()
	        #Creo que no es necesario el show
	        plt.show()
	        
	        #Setup the plot
	        self.fig, self.axes = plt.subplots(figsize=(12,12))
	        #Set x, y label and title
		label=r'A.U.($6\times10^{24}$m)'
	        self.axes.set_xlabel(label)
	        self.axes.set_ylabel(label)
	        self.axes.set_title('Solution of %s body problems' %(self.number_body))
	        
	        #To make that the same body have the same color
	        curves = [np.random.random(20) for i in self.bodies_range]
	        jet = cm = plt.get_cmap('jet') 
	        cNorm  = colors.Normalize(vmin=0, vmax=self.bodies_range[-1])
	        self.scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
	        
	        #Plot the initial positons and the radios of eacho body in function of this mass
		circles = []
	        for i in self.bodies_range:
		    name = self.grav.bodies[i].obj_id
	            x = self.grav.bodies[i].obj_position[0]
	            y = self.grav.bodies[i].obj_position[1]
	            colorVal = self.scalarMap.to_rgba(i)
	            #self.axes.plot(x, y, '^', color=colorVal)
#	            circles.append( self.axes.add_patch(plt.Circle((x,y), radius=self.circle_radio[i], color=colorVal,label=name)) )
	            circles.append( self.axes.add_patch(plt.Circle((x,y), radius=0.05, color=colorVal,label=name)) )
	        self.axes.axis('equal')
	        self.axes.margins(0)
		plt.legend()
	        plt.draw()
	        for obj in circles:
			obj.remove()
    
    def update(self,step_num):
        #x and y are position vectors for all bodys
	plot_circ = []; plot_line = []
        for i in self.bodies_range:
            x  = self.grav.bodies[i].obj_position[0]
            y  = self.grav.bodies[i].obj_position[1]
            xp = self.grav.bodies[i].obj_path[0]
            yp = self.grav.bodies[i].obj_path[1]
            colorVal = self.scalarMap.to_rgba(i)
#            plot_obj.append( self.axes.plot(x, y, 'o', color=colorVal)	)
#            plot_circ.append( self.axes.add_patch(plt.Circle((x,y), radius=self.circle_radio[i], color=colorVal)) )
            plot_circ.append( self.axes.add_patch(plt.Circle((x,y), radius=0.05, color=colorVal)) )
            plot_line.append( self.axes.plot(xp, yp, '--', color=colorVal))
	time = step_num*self.grav.step_size
	txt = plt.text(.5,.975,'time='+str(time)+'years',horizontalalignment='center',verticalalignment='center',transform = self.axes.transAxes,bbox=dict(facecolor='1'))
        plt.draw()
	for obj in plot_circ:
		print(obj)
		obj.remove()
	for obj in plot_line:
		print(obj[0])
		obj[0].remove()
	txt.remove()
