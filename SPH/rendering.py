"""
File used to control purely visual aspects of the simulation
"""
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os
import glob


class PositionData:
    def __init__(self, data, data_location=None, delimiters=None):
        if type(data) is str:
            self.positions = np.loadtxt(data_location, delimiter=delimiters)
        else:
            self.positions = data
        self.gridx = None
        self.gridy = None

    def display_positions_on_grid(self):
        plt.plot(self.positions[:, 0], self.positions[:, 1], ".", markersize=3)
        plt.show()

    def _create_grid(self, grid_size):
        x = np.linspace(-grid_size[0], grid_size[0], 2 * grid_size[0])
        y = np.linspace(-grid_size[1], grid_size[1], 2 * grid_size[1])
        x_grid, y_grid = np.meshgrid(x, y)
        self.gridx = x_grid
        self.gridy = y_grid

    def calculate_densities(self, smoothing_radius, grid_size):
        self._create_grid(grid_size)
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

    def display_densities_heatmap(self, smoothing_radius, grid_size):
        density_grid = self.calculate_densities(smoothing_radius, grid_size)
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


def _smoothing_kernel(radius, dst):
    volume = np.pi * (radius ** 8) / 4
    value = np.maximum(0, radius ** 2 - dst ** 2)
    return value ** 3 / volume


class Animation:
    def __init__(self, data_location: str, smoothing_radius, grid_size, delimiters=","):
        self.data_location = data_location
        self.positions = np.loadtxt(data_location, delimiter=delimiters, skiprows=1)
        self.density_map = np.zeros((grid_size[0] * 2, grid_size[1] * 2, int(len(self.positions[0, :]) / 2)))
        self.grid_size = grid_size
        self.smoothing_radius = smoothing_radius
        x = np.linspace(-grid_size[0], grid_size[0], 2 * grid_size[0])
        y = np.linspace(-grid_size[1], grid_size[1], 2 * grid_size[1])
        self.gridx, self.gridy = np.meshgrid(x, y)

    def calculate_densities(self):
        for i in range(self.density_map.shape[2]):
            timestep = PositionData(self.positions[:, 2 * i:2 * i + 2], self.grid_size)
            self.density_map[:, :, i] = timestep.calculate_densities(self.smoothing_radius, self.grid_size)
            # print(f"Calculated densities for timestep {i}")

    def animate_densities(self):
        frames = []  # List to store paths of frame images

        # Count existing GIF files in the outputGifs directory
        existing_gifs = glob.glob('outputGifs/density_animation*.gif')
        gif_count = len(existing_gifs) + 1  # Increment to name the new file

        for i in range(self.density_map.shape[2]):
            fig, ax = plt.subplots()
            ax.contourf(self.gridx, self.gridy, self.density_map[:, :, i], cmap='viridis')
            # Save each frame as a PNG file
            frame_filename = f'outputGifs/frame_{i}.png'
            plt.savefig(frame_filename)
            # plt.close(fig)  # Close the figure to free up memory
            frames.append(frame_filename)

        # Create GIF from saved frames
        gif_filename = f'outputGifs/density_animation ({gif_count}).gif'
        with imageio.get_writer(gif_filename, mode='I') as writer:
            for frame_filename in frames:
                image = imageio.imread(frame_filename)
                writer.append_data(image)

        # Optionally, remove the individual frame files after creating the GIF
        for frame_filename in frames:
            os.remove(frame_filename)

test = Animation("Data/AnimationTestData.txt", smoothing_radius=30, grid_size=(60, 60), delimiters=";")
test.calculate_densities()
test.animate_densities()

        # print("Animation saved as density_animation.gif")

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
