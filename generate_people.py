from __future__ import print_function
from random import random
import numpy as np

names=[
'Ambarish',
'Bruno',
'Cecilia',
'Danilo',
'David',
'Ezequiel',
'Fabio',
'Franco',
'Freddy',
'Hossein',
'Luis',
'Maria',
'Michel',
'Moustafa',
'Muhammad',
'Oscar',
'PabloH.',
'PabloN.',
'Saeed',
'Tiago',
'Vinicius',
'William',
]

line0='ID	MASS	X	Y	V_X	V_Y'

def rand(norm=1.):
	return ( norm*(2.*random()-1.))


f=open('Workshop_people.txt','w')
print(line0,file=f)
G = 0.0374038
ind=10
M=0;mass=0
for name in names:
	M	+=mass
	r	= random()*ind
#	v	= rand(.03*(ind-9))
	v	= np.sqrt(G*M/r)

	ind	+= 5.
	mass	= random()*(50-ind/5.)
	theta	= rand(np.pi)

	x	= r*np.cos(theta) 
	y	= r*np.sin(theta)
	vx	= -v*(y/r)
	vy	=  v*(x/r)

	print(name,mass,x,y,vx,vy,sep='\t',file=f)
