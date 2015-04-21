#!/usr/bin/env python3 
from __future__ import print_function
from Body import Body
from Plot import make_plot
#from toy_funcs import *
import numpy as np

def moveRK4(deltaT,bodies):
        """Integrate the movement of all the bodies listed in bodies[]"""

        #
        # This function integrates cinematic equations for all bodies in the list called "bodies"
        #
        
        # Create the matrix from discretized equations.
        # It is created to relate aal coordinates and positions, so its size is 4N x 4N
        nBodies = len(bodies)
        Aux = np.zeros(16*nBodies*nBodies)
        M = Aux.reshape(4*nBodies,4*nBodies)
        
        # Matriz M can be split into 4 subblocks: top-left (tl), top-right (tr), bottom-left (bl), bottom-right (br)
        # tl and br anly contains zeros
        # tr is diagonal (unity)
        # bl contains g_ij
        
        # Setting tr
        for i in range(2*nBodies):
            M[i][i+2*nBodies] = 1

        
        # Setting bl
        for i in range(nBodies):
            for j in range(nBodies):
                if i != j:
                    M[i+2*nBodies][j]   = bodies[i].gfactor(bodies[j])
                    M[i+3*nBodies][j+nBodies] = M[i+2*nBodies][j]
                else:
                    gsum = 0
                    for k in range(nBodies):
                        gsum += bodies[i].gfactor(bodies[k])
                    
                    M[i+2*nBodies][j]   = -gsum
                    M[i+3*nBodies][j+nBodies] = M[i+2*nBodies][j]

#        np.set_printoptions(formatter={'float': '{: 2.1g}'.format})         
#        print(M)
        
        # Setting the initial state for vector alpha (position and velocity)
        alpha     = np.zeros(4*nBodies)
        alpha_new = np.zeros(4*nBodies)

        for i in range(nBodies):    
           alpha[i]           = bodies[i].obj_position[0]    # X coordinate
           alpha[i+nBodies]   = bodies[i].obj_position[1]    # Y coordinate
           alpha[i+2*nBodies] = bodies[i].obj_velocity[0]    # Vx
           alpha[i+3*nBodies] = bodies[i].obj_velocity[1]    # Vy
         
         
        # Vector definition for RK calculation
        K1 = deltaT * np.dot(M, alpha)
        K2 = deltaT * np.dot(M, np.add(alpha,0.5*K1))
        K3 = deltaT * np.dot(M, np.add(alpha,0.5*K2))
        K4 = deltaT * np.dot(M, np.add(alpha,K3))
         
        # Advance one timestep
        alpha_new = np.add(alpha,(1./6.)*K1)
        alpha_new = np.add(alpha_new,(1./3.)*K2)
        alpha_new = np.add(alpha_new,(1./3.)*K3)
        alpha_new = np.add(alpha_new,(1./6.)*K4)    
            
        # Update bodies positions and velocities
        update(alpha_new,bodies)
         
         






def update(alpha_new,bodies):
        """update position and velocity"""
        
        nBodies = len(bodies)
        
        for i in range(nBodies):
            bodies[i].obj_position[0] = alpha_new[i]
            bodies[i].obj_position[1] = alpha_new[i+nBodies] 
            bodies[i].obj_velocity[1] = alpha_new[i+2*nBodies] 
            bodies[i].obj_velocity[1] = alpha_new[i+3*nBodies] 
            
        
