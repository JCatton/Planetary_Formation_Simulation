"""
File used to control purely visual aspects of the simulation
"""
import numpy as np
import matplotlib.pyplot as plt


class PositionData:
    def __init__(self, data_location: str, delimiters=","):
        self.data_location = data_location
        self.delimiters = delimiters
        self.positions = np.loadtxt(data_location, delimiter=delimiters)
        self.gridx = None
        self.gridy = None

    def display_positions_on_grid(self):
        plt.plot(self.positions[:, 0], self.positions[:, 1], ".", markersize=3)
        plt.show()

    def _create_grid(self, grid_size=(120, 120)):
        x = np.linspace(-grid_size[0], grid_size[0], 2*grid_size[0])
        y = np.linspace(-grid_size[1], grid_size[1], 2*grid_size[1])
        x_grid, y_grid = np.meshgrid(x, y)
        self.gridx = x_grid
        self.gridy = y_grid

    def calculate_densities(self, smoothing_radius):
        points = np.stack([self.gridx.ravel(), self.gridy.ravel()], axis=-1)  # Shape: (num_points, 2)
        # Expand dimensions for broadcasting
        sample_points_exp = np.expand_dims(points, axis=1)  # Shape: (num_points, 1, 2)
        positions_exp = np.expand_dims(self.positions, axis=0)  # Shape: (1, num_positions, 2)

        # Calculate squared distances using broadcasting
        sq_distances = np.sum((sample_points_exp - positions_exp) ** 2, axis=2)  # Shape: (num_points, num_positions)

        # Calculate influence using the smoothing kernel
        influences = _smoothing_kernel(smoothing_radius, np.sqrt(sq_distances))  # Apply sqrt to get distances

        # Sum up the influences to get densities
        densities = np.sum(influences, axis=1)  # Shape: (num_points,)

        density_grid = densities.reshape(self.gridx.shape)
        return density_grid

    def display_densities_heatmap(self, smoothing_radius=10, grid_size=(120, 120)):
        self._create_grid(grid_size)
        density_grid = self.calculate_densities(smoothing_radius)
        plt.figure(figsize=(8, 6))
        plt.contourf(self.gridx, self.gridy, density_grid, cmap='viridis')
        plt.colorbar()
        plt.title('Density Distribution')
        plt.xlabel('X axis')
        plt.ylabel('Y axis')
        plt.show()

    def add_noise_to_positions(self, number=50):
        random_particles = np.random.uniform(low=np.min(self.gridx), high=np.max(self.gridx), size=(number, 2))
        self.positions = np.vstack((self.positions, random_particles))

    def remove_noise(self):
        self.positions = np.loadtxt(self.data_location, delimiter=self.delimiters)


def _smoothing_kernel(radius, dst):
    volume = np.pi * (radius ** 8) / 4
    value = np.maximum(0, radius**2 - dst**2)
    return value**3 / volume

# #from particles import Particle
# import pylab as pl
# def calc_particle_grid_dists(grid_x, grid_y, particles: list[Particle]):
#     return [np.ndarray(np.power(np.power(grid_x - particle.position[0], 2)
#                         + np.power(grid_y - particle.position[1], 2), 0.5))
#                               for particle in particles]
#
# def find_density_at_grid_point(smoothing_kernal: callable, grid_x, grid_y, particles: list[Particle]):
#     densities = np.zeros(grid_x.shape, dtype=np.float64)
#     distances = calc_particle_grid_dists(grid_x, grid_y, particles)
#     for particle, distance in zip(particles, distances):
#         densities += smoothing_kernal(distance)

# class Animation:
#     def __init__(self, DataLocation:str, delimiters = ","):
#
#         positions = np.loadtxt(DataLocation, delimiter=delimiters)
#         self.positions = positions
#
#     def plot(self):
#         fig = plt.figure()
#         ax = fig.add_subplot()
#         ax.plot(self.positions[:,0], locations[:,1])
