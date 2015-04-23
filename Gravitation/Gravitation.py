#!/usr/bin/env python3

from __future__ import print_function

from Body import Body
from Plot import make_plot
from toy_funcs import *

import numpy as np

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
    def __init__(self,scale_mass=best_mass,scale_distance=best_distance,scale_time=best_time):
        """ 
        Compose a list and a dict with all bodies

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
        Add a body to the list with all bodies
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
        Reads bodies from a file
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
        
        
    def setUpInt(self,method,timeStep,do_plot):
        self.method = method
        self.step_size = float(timeStep)
        self.do_plot = do_plot

    def take_steps(self, number_of_steps,plot,plot_every_n):
        """
        Takes steps for all bodies
        """
        for i in range(number_of_steps):
<<<<<<< HEAD
            print('\nstep =',i)

=======
#            print('\nstep =',i)
>>>>>>> 611ae405c832d2992f19f927af64ace2de5fdaf8
            self.move()
            
            positions_array = self.position_array()
            
            if self.do_plot == True and i%plot_every_n==0: 
                plot.update(i, positions_array)

            self.nStep+=1
       
        print("\nRun for ", self.nBodies," bodies during ", number_of_steps ," time steps\n")


    def move(self):
        """
        Integrate the movement of all the bodies listed in bodies[]

        This function integrates cinematic equations for all bodies in the list called "bodies"
        """

        #
        # This function integrates cinematic equations for all bodies in the list called "bodies"
        #
        
        nBodies = self.nBodies
        deltaT = self.step_size
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
        
        else:
            if self.method == "euler":
                # Euler explicito
                K1 = deltaT * np.dot(self.M, self.alpha)
                self.alpha_new = np.add(self.alpha,K1)

            elif self.method == "cn":
                # Crank-Nicholson
                I = np.identity(4*nBodies) 
                K1 =  np.add(I, (-deltaT/2)*self.M)
                K2 =  np.add(I, (deltaT/2)*self.M)
                K3 = np.linalg.inv(K1)
                K4 = np.dot(K3,K2)
                self.alpha_new = np.dot(K4,self.alpha)

        # Update bodies positions and velocities
        self.update()


    def update(self):
        """
        Update position, velocity and the path
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
        x = []
        y = []
        xp = []
        yp = []
        for body in self.bodies:
            x.append(body.obj_position[0])
            y.append(body.obj_position[1])
            xp.append(body.obj_path[0])
            yp.append(body.obj_path[1])

        return([x, y, xp, yp])
