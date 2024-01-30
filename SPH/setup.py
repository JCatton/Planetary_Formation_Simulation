import numpy as np
from random import random
def kernal(name: str) -> callable:
    match name:
        case "Linear":
            return lambda x: 1 - x if x < 1 else 0
        case default:
            return

def grid_init(grid_height, grid_width, height_points, width_points) -> (np.ndarray, np.ndarray):
    x = np.linspace(0, grid_height, height_points)
    y = np.linspace(0, grid_width, width_points)
    return np.meshgrid(x, y)

def particle_init(max_height, max_width, max_velocity, max_mass, number_of_particles) -> np.ndarray:
    positions = np.random.rand(number_of_particles, 2)
    positions[:, 0] *= max_height
    positions[:, 1] *= max_width
    velocities = np.random.rand(number_of_particles, 2) * max_velocity
    mass = np.full(max_mass, number_of_particles, dtype=np.float64)
    return positions, velocities, mass