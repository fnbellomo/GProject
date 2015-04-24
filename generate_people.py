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
ind=0;dind=2.;theta=0
M=0;mass=50
print('ICTP',mass,0,0,0,0,sep='\t',file=f)
for i in range(12):
	name=names[i]

	M	+=mass
	ind	+= dind

	mass	= random()*(100./(10.+ind/dind))
	r	= (1+rand(.2))*ind
	v	= np.sqrt(G*M/r)
#	r	= random()*ind
#	v	= rand(.03*(ind-9))

	theta	+= np.pi*.37

	x	= r*np.cos(theta) 
	y	= r*np.sin(theta)
	vx	= -v*(y/r)
	vy	=  v*(x/r)

	print(name,mass,x,y,vx,vy,sep='\t',file=f)
	print(name,mass,x,y,vx,vy,sep='\t')
for i in range(12,22,2):
	name	= names[i]

	M	+=mass
	ind	+= dind

	mass	= random()*(100./(10.+ind/dind-12.))
	r	= (1+rand(.2))*ind
	v	= np.sqrt(G*M/r)
#	r	= random()*ind
#	v	= rand(.03*(ind-9))

	theta	+= np.pi*.37

	x	= r*np.cos(theta) 
	y	= r*np.sin(theta)
	vx	= -v*(y/r)
	vy	=  v*(x/r)

	print(name,mass,x,y,vx,vy,sep='\t',file=f)
	print(name,mass,x,y,vx,vy,sep='\t')

	name2	= names[i+1]

	mass2	= .05*mass
	dr	= 1
	r2	= r+dr
	v2	= v+np.sqrt(G*mass/dr)
#	r	= random()*ind
#	v	= rand(.03*(ind-9))

	x2	= r2*np.cos(theta) 
	y2	= r2*np.sin(theta)
	vx2	= -v2*(y2/r2)
	vy2	=  v2*(x2/r2)

	print(name2,mass2,x2,y2,vx2,vy2,sep='\t',file=f)
	print(name2,mass2,x2,y2,vx2,vy2,sep='\t')
