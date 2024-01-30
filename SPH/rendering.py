"""
File used to control purely visual aspects of the simulation
"""
import numpy as np
from particles import Particle
def calc_particle_grid_dists(grid_x, grid_y, particles: list[Particle]):
    return [np.ndarray(np.power(np.power(grid_x - particle.position[0], 2) + np.power(grid_y - particle.position[1], 2), 0.5)) for particle in particles]

def find_density_at_grid_point(smoothing_kernal: callable, grid_x, grid_y, particles: list[Particle]):
    densities = np.zeros(grid_x.shape, dtype=np.float64)
    distances = calc_particle_grid_dists(grid_x, grid_y, particles)
    for particle, distance in zip(particles, distances):
        densities += smoothing_kernal(distance)




