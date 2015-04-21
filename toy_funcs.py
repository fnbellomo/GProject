import pylab as plt

def step_func(step_size,obj_id,bodies_list,dict_bodies):
	body	= dict_bodies[obj_id]
	for i in range(2):
		body.obj_position[i] += step_size*body.obj_velocity[i]
		body.obj_velocity[i] -= step_size*body.obj_position[i]
	return body.obj_position, body.obj_velocity
def print_func(bodies_list):
	for body in bodies_list:
		coord	= body.obj_position
		x,y	= coord[0],coord[1]
		plt.plot(x,y,'o',color='b',ms=1)
	plt.ion()
	plt.draw()
#	plt.show()
