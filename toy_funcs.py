import pylab as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx

def step_func(step_size,obj_id,bodies_list,dict_bodies):
	body	= dict_bodies[obj_id]
	for i in range(2):
		body.obj_position[i] += step_size*body.obj_velocity[i]
		body.obj_velocity[i] -= step_size*body.obj_position[i]
	return body.obj_position, body.obj_velocity
def print_func(bodies_list,first):
	ind=0
	for body in bodies_list:
		name	= body.obj_id
		coord	= body.obj_position
		x,y	= coord[0],coord[1]
		plt.plot(x,y,'o',color=cmx.ScalarMappable(norm=colors.Normalize(vmin=0, vmax=len(bodies_list)),cmap=plt.get_cmap('jet')).to_rgba(ind),ms=2,label=name)
		ind	+=1
	if first == True: plt.legend()
	plt.ion()
	plt.draw()
#	plt.show()
