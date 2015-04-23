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

#To check if exist a dir
import os
import shutil

from math import sqrt

class make_plot(object):
    """
    Class to make the plots in run time
    
    Parameters 
    ---------- 
    grav : Gravitacional Object

    This class is responsible for making the plots of simulated orbits of the problem of n-bodies. 
    To create a make_plot object requires a Gravitational object. 
    If Gravitational().do_plot == True, the plot is done. In contratio case, no.
    """

    def __init__(self, grav):
        """
        Create the class

        If Gravitational().do_plot == True, make the plots
        """

        self.grav = grav
        self.number_body = len(self.grav.bodies)
        self.bodies_range = range(self.number_body)

        self.mass = [grav.bodies[i].obj_mass for i in range(len(grav.bodies))]
        self.mass_max = max(self.mass)
        self.rad  = [sqrt(pow(grav.bodies[i].obj_position[0],2)+pow(grav.bodies[i].obj_position[1],2)) for i in range(len(grav.bodies))]
        self.rad_max = max(self.rad)
        self.circle_radio = [ self.rad_max*0.1*m/self.mass_max for m in self.mass]
        
        #Check if are some img in the path.
        #If exist, delete all
        self.img_path = './Gravitation/Animation/Img/'
        if os.path.isdir(self.img_path):
            shutil.rmtree(self.img_path)
            os.mkdir(self.img_path)
        else:
            os.mkdir(self.img_path)

        #img_num va a ser un contador que va a aumentar, 
        #con el cual vamos a guardar
        #cada imagen que generamos para luego hacer una animacion.
        self.img_num = 1

        if grav.do_plot == True:
            #Turn interactive mode on.
            plt.ion()
	        
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
	        
	    #Plot the initial positons and the radios of each body in function of this mass
	    circles = []
	    for i in self.bodies_range:
		name = self.grav.bodies[i].obj_id
	        x = self.grav.bodies[i].obj_position[0]
	        y = self.grav.bodies[i].obj_position[1]
	        colorVal = self.scalarMap.to_rgba(i)
	        #self.axes.plot(x, y, '^', color=colorVal)
	        circles.append( self.axes.add_patch(plt.Circle((x,y), radius=self.circle_radio[i], color=colorVal,label=name)) )
	    self.axes.axis('equal')
	    self.axes.margins(0)
	    plt.legend()
	    plt.draw()
	    for obj in circles:
		obj.remove()

	    #Plot the initial positons and the radios of eacho body in function of this mass
            circles = []
            for i in self.bodies_range:
                name = self.grav.bodies[i].obj_id
                x = self.grav.bodies[i].obj_position[0]
                y = self.grav.bodies[i].obj_position[1]
                colorVal = self.scalarMap.to_rgba(i)
                circles.append( self.axes.add_patch(plt.Circle((x,y), radius=self.circle_radio[i], color=colorVal,label=name)) )

            self.axes.axis('equal')
            plt.legend()
            plt.grid(True)
            plt.draw()

            for obj in circles:
                obj.remove()

            #save the plot
            self.save_img()
    
    def update(self,step_num):
        """
        Update the new points in the plots

        parameters
        ----------
        step_num : Number of step
        """

        #x and y are position vectors for each bodys
        plot_circ = []
        plot_line = []

        for i in self.bodies_range:
            x  = self.grav.bodies[i].obj_position[0]
            y  = self.grav.bodies[i].obj_position[1]
            xp = self.grav.bodies[i].obj_path[0]
            yp = self.grav.bodies[i].obj_path[1]

            colorVal = self.scalarMap.to_rgba(i)
#            plot_obj.append( self.axes.plot(x, y, 'o', color=colorVal)	)
            plot_circ.append( self.axes.add_patch(plt.Circle((x,y), radius=self.circle_radio[i], color=colorVal)) )
            plot_line.append( self.axes.plot(xp, yp, '--', color=colorVal))

        time = step_num*self.grav.step_size
        txt = plt.text(.5,.975,'time='+str(time)+'years',horizontalalignment='center',verticalalignment='center',\
                        transform = self.axes.transAxes,bbox=dict(facecolor='1'))
        plt.draw()

        for obj in plot_circ:
            obj.remove()
        for obj in plot_line:
            obj[0].remove()

        txt.remove()

        #save the plot
        self.save_img()


    def save_img(self):
        """
        Method to save the plots to later make a animations
        """
        img_name = self.img_path+str(self.img_num)+'.png'
        self.fig.savefig(img_name)
        self.img_num += 1
