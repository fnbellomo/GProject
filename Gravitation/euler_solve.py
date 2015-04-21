import math


# this calculate the attraction force between the body and other body
def attraction(self, other):

    # Compute the distance of the other body.
    sx, sy = self.px, self.py
    ox, oy = other.px, other.py
    dx = (ox-sx)
    dy = (oy-sy)
    d = math.sqrt(dx**2 + dy**2)

    # Compute the force of attraction
    f = G * self.mass * other.mass / (d**2)
    
    # Compute the direction of the force.
    theta = math.atan2(dy, dx)
    fx = math.cos(theta) * f
    fy = math.sin(theta) * f
    return fx, fy


def iteration(bodies)
    # Add up all of the forces exerted on 'body'.
    total_fx = total_fy = 0.0
    for other in bodies:
        # Don't calculate the body's attraction to itself
        if body is other:
            continue
        fx, fy = body.attraction(other)
        total_fx += fx
        total_fy += fy

        # Record the total force exerted.
        force[body] = (total_fx, total_fy)

        # Update velocities based upon on the force.
        for body in bodies:
            fx, fy = force[body]
            body.vx += fx / body.mass * timestep
            body.vy += fy / body.mass * timestep

            # Update positions
            body.px += body.vx * timestep
            body.py += body.vy * timestep
 

