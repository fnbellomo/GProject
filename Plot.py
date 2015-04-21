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

    def __init__(self, body_numbers):
        self.body_numbers = body_numbers
        #Turn interactive mode on.
        plt.ion()
        #Creo que no es necesario el show
        plt.show()

        #Setup the plot
        self.fig, self.axes = plt.subplots(figsize=(12,3))

        #Set x, y label and title
        self.axes.set_xlabel(r'$x$')
        self.axes.set_ylabel(r'$y$')
        self.axes.set_title('Solution of %s body problems' %(self.body_numbers))

        #To make that the same body have the same color
        body_range = range(self.body_numbers)
        curves = [np.random.random(20) for i in body_range]
        jet = cm = plt.get_cmap('jet') 
        cNorm  = colors.Normalize(vmin=0, vmax=body_range[-1])
        self.scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)

    #Update the plots
    def update(self, x, y):
        #x and y are position vectors for all bodys
        for i in range(self.body_numbers):
            colorVal = self.scalarMap.to_rgba(i)
            self.axes.plot(x[i], y[i], 'o', color=colorVal)
        plt.draw()
