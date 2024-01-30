"""
The Main Simulation Runfile
"""
from SPH import setup
number_of_particles: int = 10
grid_height: float = 100.
grid_width: float = 100.
height_points: int = 10
width_points: int = 11
particle_mass: 1
smooth_function: str = 'default'

grid_x, grid_y = setup.grid_init(grid_height, grid_width, height_points, width_points)
positions, velocities, mass = setup.particle_init(grid_height, grid_width)