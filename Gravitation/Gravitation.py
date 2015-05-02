#!/usr/bin/env python3

from __future__ import print_function

from Body import Body
from Plot import make_plot
from toy_funcs import *

import numpy as np
from math import sqrt

#To make the plots with multiprocesing
from multiprocessing import Process, Array, Value
import ctypes

import os
import time


def float_list(LIST): 
    return [float(l) for l in LIST]

# distance : 1.5E+11 m (averange distance beetween Earth to sun)
# mass : 5.9736E+24 kg (Earth mass)
# time: 3.1104E07: 
best_mass	= 1.5E+11
best_distance	= 5.9736E+24 
best_time	= 3.1104E07

class Gravitation(object):
    """
    This class is the main Gravitaion wrapper
    """
    def __init__(self, scale_mass=best_mass, scale_distance=best_distance, scale_time=best_time):
        """ 
        Compose a list with all Bodies Object and a dict with propertis.

        Parameters
        ----------
        scale_mass : float
                    Scale of mass
        scale_distance : float
                    Scale of distance
        scale_time : float
                    Scale of time

	    .bodies  corresponds to a list with the bodies, i. e. [Body1,Body2,...]		=> GRAV.bodies[1]   = Body1 
	    .lookup  corresponds to a dict with the bodies, i. e. dict([id1,Body1],...)	=> GRAV.lookup[id1] = Body1
	"""
        self.bodies	= []
        self.lookup	= dict([[body.obj_id,body] for body in self.bodies])
        self.convert_m	= scale_mass	/ best_mass	
        self.convert_r	= scale_distance/ best_distance
        self.convert_t	= scale_time	/ best_time	
        self.convert_v	= self.convert_r/ self.convert_t
        self.nStep      = 0

    def add_body(self, obj_id, obj_mass, obj_position, obj_velocity):
        """
        Add a Body Object to the list.

        This method call Body() obtects to creater a new and append to this list.

        Parameters
        ----------
        obj_id : str
                Body name
        obj_mass : float
                Body mass
        obj_position : array_like
                Position in x (float) and y (float). [x, y]
        obj_velocity : array_like
                velocity in x (float) and y (float). [V_x, V_y]
        """
        # All dimensions are scaled
        mass		= float(obj_mass)*self.convert_m
        position	= [pos*self.convert_r for pos in obj_position]	
        velocity	= [vel*self.convert_v for vel in obj_velocity]	
        new_Body	= Body(obj_id,mass,position,velocity)

        self.bodies.append( new_Body )
        self.lookup[obj_id] = new_Body
        print('*** Body = ',obj_id, obj_mass, obj_position, obj_velocity,' added ***',sep='\t')


    def import_bodies(self, filename):
        """ 
        Reads bodies from a file.

        Call add_body method for each body in the file.
        The first line of this file is't read.
        The data must be separate with a blank space.

        Parameter
        ---------
        filename : str
                 The file path to extract the data from the bodies.
        """
        file_in	= open(filename,'r')
        lines	= file_in.readlines ()
        file_in.close ()
        for i in range(1,len(lines)):
            if lines[i] != "\n" :
                aux = lines[i].split ()
                self.add_body(aux[0],aux[1],float_list(aux[2:4]),float_list(aux[4:6]))
			
        # Creation of force matrix
        self.nBodies = len(self.bodies)
        FMat = np.zeros(16*self.nBodies*self.nBodies)
        self.M = FMat.reshape(4*self.nBodies,4*self.nBodies)
        self.alpha     = np.zeros(4*self.nBodies)
        self.alpha_new = np.zeros(4*self.nBodies)
        self.alpha_new_1 = np.zeros(4*self.nBodies)
        self.alpha_new_2 = np.zeros(4*self.nBodies)

        # Computing internal energy
        self.total_energy = self.energy()
        
        
    def setUpInt(self, method, timeStep, do_plot):
        """
        Initial configuration

        Parameters
        ----------
        method : str
               Method by which it is to do the numerical integration. Can by 'runge-kutta4' or 'euler'.
        timeStep : float
               Forward time.
        do_plot : bool
               Is True, the plots is going to be display.
        """

        self.method = method
        self.step_size = float(timeStep)
        self.do_plot = do_plot


    def energy(self):
        """
        Return the total energy of the sistem (kinetic + potential).
        """
        kinetic = 0
        for body in self.bodies:
            k = 0.5 * body.obj_mass * sqrt(pow(body.obj_velocity[0],2) + pow(body.obj_velocity[1],2))
            kinetic += k

        potential = 0
        for i in range(len(self.bodies)):
            for j in range(len(self.bodies)):
                if i != j:
                    dist = sqrt(pow(self.bodies[i].obj_position[0]-self.bodies[j].obj_position[0],2) + pow(self.bodies[i].obj_position[1]-self.bodies[j].obj_position[1],2))
                    u = -0.5 * self.bodies[i].obj_mass * self.bodies[j].obj_mass / dist
                    potential += u

        return kinetic + potential

    def energy_vector(self,alphaVec):
        """
        Return the energy of the system, like Energy method but 

        Parameters
        ----------
        alphaVec : array_like
                   Is a 
        """
        nBodies = len(self.bodies)
        kinetic = 0
        for i in range(nBodies):
            k = 0.5 * self.bodies[i].obj_mass * sqrt(pow(alphaVec[i+2*nBodies],2) + pow(alphaVec[i+3*nBodies],2))
            kinetic += k

        potential = 0
        for i in range(nBodies):
            for j in range(nBodies):
                if i != j:
                    dist = sqrt(pow(alphaVec[i]-alphaVec[j],2) + pow(alphaVec[i+nBodies]-alphaVec[j+nBodies],2))
                    u = -0.5 * self.bodies[i].obj_mass * self.bodies[j].obj_mass / dist
                    potential += u

        return kinetic + potential


    def take_steps(self, number_of_steps, plot, plot_every_n):
        """
        Takes steps for all bodies.

        Solve numericaly the n-body problems using RK4 o Euler method.

        Parameter
        ---------
        number_of_steps : float
                 Total number of time steps.
        plot : object
                 make_plot Object.
        plot_every_n : float
                 Every few time steps are going on a plot.
        """
        for i in range(number_of_steps):
            self.move()
            
            positions = self.position_array()
            
            if self.do_plot == True and i%plot_every_n==0: 
                plot.update(i, positions)

            self.nStep+=1
       
        print("\nRun for ", self.nBodies," bodies during ", number_of_steps ," time steps\n")

    def save_plot(self, number_of_steps,plot,plot_every_n):
        """
        Saves plots in a file.
        """
        plot.save_all_img(number_of_steps,plot_every_n,self.position_array())

    ###################################################################
    #Testing the plot with multiprocesing
    ###################################################################

    def rk_fun_task(self, number_of_steps, plot_every_n, shared_array, end_plot, counter):
        """
        Runge Kutan task to use in multiprocessing.

        Parameters
        ----------
        number_of_steps : float
                 Total number of time steps.
        plot_everly_n : float
                 Every few time steps are going on a plot.
        shared_array : array_like
                 Shared array to pass the new calculate values from this method to plot_fun_task method.
        end_plot : int
                 Shared counter to end the plot_fun process.
        counter : int
                 Shared counter.
        """
        print('RK: PID', os.getpid())
        
        for j in range(0, number_of_steps, plot_every_n):

            for cont in range(plot_every_n):
                self.move()

            number_body = len(self.bodies)
            bodies_range = range(number_body)
            
            for i in bodies_range:
                shared_array[0][i] = self.bodies[i].obj_position[0]
                shared_array[1][i] = self.bodies[i].obj_position[1]

            counter.value += 1
            #print('RK: PID', os.getpid())
#            time.sleep(0.5)
        
        end_plot.value += 1

    def plot_fun_task(self, old_counter, shared_array, end_plot, counter, plot):
        """
        Plot function task to use in multiprocessing

        Parameters
        ----------
        old_counter : int
               Control counter.
        shared_array : array_like
               Shared array with the new values to plot.
        end_plot : int
               Shared counter to end the plot_fun process.
        counter : int
               Shared counter.
        plot : object
              make_plot Objects.
        """
        print('PLOT: PID', os.getpid())
        while end_plot.value == 1:
            """
            if counter.value == old_counter:
                print('PLOT: PID', os.getpid())
                plot.update_multiprosessing(counter.value, shared_array)
                old_counter += 1
            """
            plot.update_multiprosessing(counter.value, shared_array)
   

    def steps_multiprocessing(self, number_of_steps, plot, plot_every_n):
        """ 
        Equal to take_steps but using multiprocesing.

        Parameters
        ----------
        number_of_steps : float
                 Total number of time steps.
        plot : object
                 make_plot Object.
        plot_every_n : float
                 Every few time steps are going on a plot.
        """
        
        shared_array_base = Array(ctypes.c_double, len(self.bodies)*2)
        shared_array = np.ctypeslib.as_array(shared_array_base.get_obj())
        shared_array = shared_array.reshape(2, len(self.bodies))

        counter = Value(ctypes.c_int64, 0)
        end_plot = Value(ctypes.c_int8, 1)

        old_counter = 1
        rk_fun = Process(target = self.rk_fun_task, args=(number_of_steps, plot_every_n, shared_array, end_plot, counter))
        plot_fun = Process(target = self.plot_fun_task, args=(old_counter, shared_array, end_plot, counter, plot))

        rk_fun.start()
        plot_fun.start()

        rk_fun.join()
        plot_fun.join()

    ##################################################################


    def move(self):
        """
        Integrate the movement of all the bodies listed in bodies[]

        This function integrates cinematic equations for all bodies in the list called "bodies"
        The method can be "runge-kutta4", "euler" or "adaptive-rk4".
        """

        nBodies = self.nBodies
        # Matriz M can be split into 4 subblocks: top-left (tl), top-right (tr), bottom-left (bl), bottom-right (br)
        # tl and br anly contains zeros
        # tr is diagonal (unity)
        # bl contains g_ij
        
        # Setting tr
        for i in range(2*nBodies):
            self.M[i][i+2*nBodies] = 1
        
        # Setting bl
        for i in range(nBodies):
            for j in range(nBodies):
                if i != j:
                    self.M[i+2*nBodies][j]   = self.bodies[i].gfactor(self.bodies[j])
                    self.M[i+3*nBodies][j+nBodies] = self.M[i+2*nBodies][j]
                else:
                    gsum = 0
                    for k in range(nBodies):
                        gsum += self.bodies[i].gfactor(self.bodies[k])
                    
                    self.M[i+2*nBodies][j]   = -gsum
                    self.M[i+3*nBodies][j+nBodies] = self.M[i+2*nBodies][j]
        
        # Setting the initial state for vector alpha (position and velocity)
        for i in range(nBodies):    
            self.alpha[i]           = self.bodies[i].obj_position[0]    # X coordinate
            self.alpha[i+nBodies]   = self.bodies[i].obj_position[1]    # Y coordinate
            self.alpha[i+2*nBodies] = self.bodies[i].obj_velocity[0]    # Vx
            self.alpha[i+3*nBodies] = self.bodies[i].obj_velocity[1]    # Vy
        
        deltaT = self.step_size
        if self.method == "runge-kutta4":
            # Vector definition for RK calculation
            K1 = deltaT * np.dot(self.M, self.alpha)
            K2 = deltaT * np.dot(self.M, np.add(self.alpha,0.5*K1))
            K3 = deltaT * np.dot(self.M, np.add(self.alpha,0.5*K2))
            K4 = deltaT * np.dot(self.M, np.add(self.alpha,K3))
             
            # Advance one timestep
            self.alpha_new = np.add(self.alpha,(1./6.)*K1)
            self.alpha_new = np.add(self.alpha_new,(1./3.)*K2)
            self.alpha_new = np.add(self.alpha_new,(1./3.)*K3)
            self.alpha_new = np.add(self.alpha_new,(1./6.)*K4)

            #print(self.energy())
        else:
            if self.method == "euler":
                # Euler explicito
                K1 = deltaT * np.dot(self.M, self.alpha)
                self.alpha_new = np.add(self.alpha,K1)

            else:
                if self.method == "cn":
                    # Crank-Nicholson
                    I = np.identity(4*nBodies) 
                    K1 =  np.add(I, (-deltaT/2)*self.M)
                    K2 =  np.add(I, (deltaT/2)*self.M)
                    K3 = np.linalg.inv(K1)
                    K4 = np.dot(K3,K2)
                    self.alpha_new = np.dot(K4,self.alpha)

                else:
                    if self.method == "adaptive-rk4":
                      
                        chosenStep = False
                        while(chosenStep == False):
                            ecount = self.energy()
                        
                            # Vector definition for RK calculation
                            K1 = deltaT * np.dot(self.M, self.alpha)
                            K2 = deltaT * np.dot(self.M, np.add(self.alpha,0.5*K1))
                            K3 = deltaT * np.dot(self.M, np.add(self.alpha,0.5*K2))
                            K4 = deltaT * np.dot(self.M, np.add(self.alpha,K3))
                 
                            # Advance one timestep
                            self.alpha_new = np.add(self.alpha,(1./6.)*K1)
                            self.alpha_new = np.add(self.alpha_new,(1./3.)*K2)
                            self.alpha_new = np.add(self.alpha_new,(1./3.)*K3)
                            self.alpha_new = np.add(self.alpha_new,(1./6.)*K4)
                            self.alpha_new_1 = np.copy(self.alpha_new)
                            
                            ecount_end = self.energy_vector(self.alpha_new)
                            energy_loss = abs((ecount_end - ecount) / self.total_energy)
                            #print(energy_loss)
                            if energy_loss > 0.000001:
                                deltaT = deltaT / 2

                            else:
                                chosenStep = True

        # Update bodies positions and velocities
        self.update()


    def update(self):
        """
        Update position, velocity and the path in all Body objects.
        """
        
        nBodies = self.nBodies
        
        for i in range(nBodies):
            self.bodies[i].obj_position[0] = self.alpha_new[i]
            self.bodies[i].obj_position[1] = self.alpha_new[i+nBodies] 
            self.bodies[i].obj_velocity[0] = self.alpha_new[i+2*nBodies] 
            self.bodies[i].obj_velocity[1] = self.alpha_new[i+3*nBodies]
            self.bodies[i].obj_path[0] 	   .append(self.bodies[i].obj_position[0])
            self.bodies[i].obj_path[1] 	   .append(self.bodies[i].obj_position[1])

    def position_array(self):
        """
        Retorna 1 lista con 4 arrays. Dos de las posiciones en x e y de todos los cuerpos. Los otros dos son los path en x e y de cada cuerpo.

        Este array se lo paso a el metodo plot para actualizar los puntos
        """
        xp = []
        yp = []

        for body in self.bodies:
            xp.append(body.obj_path[0])
            yp.append(body.obj_path[1])

        return [xp, yp]
