#!/usr/bin/env python3 
from __future__ import print_function
from Body import Body
from Plot import make_plot
from toy_funcs import *

def float_list(LIST): return [float(l) for l in LIST]

class Gravitation(object):
    """
    This class is the main Gravitaion wrapper
    """
    def __init__(self):
        """ Compose a list and a dict with all bodies 
		.bodies  corresponds to a list with the bodies, i. e. [Body1,Body2,...]		=> GRAV.bodies[1]   = Body1 
		.lookup  corresponds to a dict with the bodies, i. e. dict([id1,Body1],...)	=> GRAV.lookup[id1] = Body1
	"""
        self.bodies	= []
        self.lookup	= dict([[body.obj_id,body] for body in self.bodies])
	self.step_size	= 0.1
    def add_body(self, obj_id, obj_mass, obj_position, obj_velocity):
        """ Add a body to the list with all bodies """
	new_Body	= Body(obj_id, obj_mass, obj_position, obj_velocity)
	self.bodies.append( new_Body )
	self.lookup[obj_id] = new_Body
	print('*** Body = ',obj_id, obj_mass, obj_position, obj_velocity,' added ***',sep='\t')
    def import_bodies(self, filename):
        """ Reads bodies from a file """
	file_in	= open(filename,'r')
	lines	= file_in.readlines ()
	file_in.close ()
	for i in range(1,len(lines)):
		if lines[i] != "\n" :
			aux = lines[i].split ()
			self.add_body(aux[0],aux[1],float_list(aux[2:4]),float_list(aux[4:6]))
#			self.add_body(obj_id, obj_mass, obj_position, obj_velocity)

    def take_steps(self, number_of_steps, step_func,plot):
        """ Takes steps for all bodies """
	for i in range(number_of_steps):
		print('\nstep =',i)
		for body in self.bodies:
			body.step(step_func, self.step_size, self.bodies, self.lookup)
		self.print_status(plot)
    def print_status(self,plot):
        """ Print the position for all bodies """
#	print_func(self.bodies,first_step)
	plot.update()
#        try:
#                acc.withdraw(amount)
#        except NotEnoughFundsException:
#                print("Dear client, you should check your balance before performing this operation")

    def moveRK4(self, deltaT):
        """Integrate the movement of all the bodies listed in bodies[]"""

        #
        # This function integrates cinematic equations for all bodies in the list called "bodies"
        #
        
        # Create the matrix from discretized equations.
        # It is created to relate aal coordinates and positions, so its size is 4N x 4N
        nBodies = len(self.bodies)
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
                    M[i+2*nBodies][j]   = self.bodies[i].gfactor(self.bodies[j])
                    M[i+3*nBodies][j+nBodies] = M[i+2*nBodies][j]
                else:
                    gsum = 0
                    for k in range(nBodies):
                        gsum += self.bodies[i].gfactor(self.bodies[k])
                    
                    M[i+2*nBodies][j]   = -gsum
                    M[i+3*nBodies][j+nBodies] = M[i+2*nBodies][j]

#        np.set_printoptions(formatter={'float': '{: 2.1g}'.format})         
#        print(M)
        
        # Setting the initial state for vector alpha (position and velocity)
        alpha     = np.zeros(4*nBodies)
        alpha_new = np.zeros(4*nBodies)

        for i in range(nBodies):    
           alpha[i]           = self.bodies[i].obj_position[0]    # X coordinate
           alpha[i+nBodies]   = self.bodies[i].obj_position[1]    # Y coordinate
           alpha[i+2*nBodies] = self.bodies[i].obj_velocity[0]    # Vx
           alpha[i+3*nBodies] = self.bodies[i].obj_velocity[1]    # Vy
         
         
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
        self.update(alpha_new)
         
         






    def update(self, alpha_new):
        """update position and velocity"""
        
        nBodies = len(self.bodies)
        
        for i in range(nBodies):
            self.bodies[i].obj_position[0] = alpha_new[i]
            self.bodies[i].obj_position[1] = alpha_new[i+nBodies] 
            self.bodies[i].obj_velocity[1] = alpha_new[i+2*nBodies] 
            self.bodies[i].obj_velocity[1] = alpha_new[i+3*nBodies] 
            
        
