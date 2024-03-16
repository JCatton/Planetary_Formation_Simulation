"""
File used to control purely visual aspects of the simulation
"""
import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import os
import glob
# Define the smoothing kernel function


def smoothing_kernel(radius, dst):
    volume = np.pi * (radius ** 8) / 4
    value = np.maximum(0, radius ** 2 - dst ** 2)
    return value ** 3 / volume


class PositionData:
    def __init__(self, data_location=None, delimiters=None):
        if data_location and os.path.exists(data_location):
            self.positions = np.loadtxt(data_location, delimiter=delimiters)
        else:
            self.positions = None
        self.grid = None

    def display_positions_on_grid(self):
        plt.plot(self.positions[:, 0], self.positions[:, 1], ".", markersize=3)
        plt.show()

    def _create_grid(self, x_size: tuple[int, int], y_size: tuple[int, int]):
        x = np.linspace(x_size[0], x_size[1], x_size[1] - x_size[0] + 1)
        y = np.linspace(y_size[0], y_size[1], y_size[1] - y_size[0] + 1)
        self.grid = np.meshgrid(x, y)

    def calculate_densities(self, smoothing_radius, x_size: tuple[int, int], y_size: tuple[int, int]):
        if self.positions is None:
            raise ValueError("Position data not loaded.")
        self._create_grid(x_size, y_size)
        points = np.stack([self.grid[0].ravel(), self.grid[1].ravel()], axis=-1)
        sq_distances = np.sum((points[:, np.newaxis, :] - self.positions[np.newaxis, :, :]) ** 2, axis=2)
        influences = smoothing_kernel(smoothing_radius, sq_distances)
        densities = np.sum(influences, axis=1)
        return densities.reshape(self.grid[0].shape)

    def display_densities_heatmap(self, smoothing_radius, x_size: tuple[int, int], y_size: tuple[int, int]):
        density_grid = self.calculate_densities(smoothing_radius, x_size, y_size)
        plt.figure(figsize=(10, 8))
        plt.contourf(self.grid[0], self.grid[1], density_grid, levels=40)
        plt.colorbar()
        plt.title('Density Distribution')
        plt.xlabel('X axis')
        plt.ylabel('Y axis')
        plt.tight_layout()
        plt.show()


# Will fix grids on this tomorrow ≈ 13:00/14:00 ish
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

# test = Animation("Data/AnimationTestData.txt", smoothing_radius=30, grid_size=(1000, 120), delimiters=";")
# test.calculate_densities()
# test.animate_densities()

# Old Jonte Stuffs
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
