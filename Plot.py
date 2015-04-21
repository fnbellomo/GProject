#!/usr/bin/env python3 
from __future__ import print_function

import matplotlib
#To make interactive plots, I need use TK
matplotlib.use('TkAgg')
#Matplotlib configuration parameters:
matplotlib.rcParams.update({'font.size': 18, 'text.usetex': True})

import matplotlib.pyplot as plt

#To make the same body have the same color
import matplotlib.colors as colors
import matplotlib.cm as cmx

class make_plot():
    """
    Class to make the plots in run time
    """

    def __init__(self, grav):
        self.grav = grav
        self.number_body = len(self.grav.bodies)
        self.bodies_range = range(self.number_body)
        
        #Turn interactive mode on.
        plt.ion()
        #Creo que no es necesario el show
        plt.show()
        
        #Setup the plot
        self.fig, self.axes = plt.subplots(figsize=(12,3))
        #Set x, y label and title
        self.axes.set_xlabel(r'$x$')
        self.axes.set_ylabel(r'$y$')
        self.axes.set_title('Solution of %s body problems' %(self.number_body))
        
        #To make that the same body have the same color
        curves = [np.random.random(20) for i in self.bodies_range]
        jet = cm = plt.get_cmap('jet') 
        cNorm  = colors.Normalize(vmin=0, vmax=self.bodies_range[-1])
        self.scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
        
        #Plot the initial positons and the radios of eacho body in function of this mass
        mass = [grav.bodies[i].obj_mass for i in range(len(grav.bodies))]
        mass_max = max(mass)
        for i in self.bodies_range:
            x = self.grav.bodies[i].obj_position[0]
            y = self.grav.bodies[i].obj_position[1]
            circle_radio = mass[i]/mass_max
            colorVal = self.scalarMap.to_rgba(i)
            #self.axes.plot(x, y, '^', color=colorVal)
            self.axes.add_patch(plt.Circle((x,y), radius=circle_radio, color=colorVal))
        self.axes.axis('equal')
        self.axes.margins(0)
        plt.draw()
    
    def update(self):
        #x and y are position vectors for all bodys
        for i in self.bodies_range:
            x = self.grav.bodies[i].obj_position[0]
            y = self.grav.bodies[i].obj_position[1]
            colorVal = self.scalarMap.to_rgba(i)
            self.axes.plot(x, y, 'o', color=colorVal)
        plt.draw()
