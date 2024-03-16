"""
File used to control purely visual aspects of the simulation
"""
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import imageio
from scipy.spatial import cKDTree



# Define the smoothing kernel function

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', s)]


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
        # Faster method for <≈ 48000

        if len(self.positions) < 40000 and x_size[1] < 150 and y_size[1] < 150:
            self._create_grid(x_size, y_size)
            points = np.stack([self.grid[0].ravel(), self.grid[1].ravel()], axis=-1)
            sq_distances = np.sum((points[:, np.newaxis, :] - self.positions[np.newaxis, :, :]) ** 2, axis=2)
            influences = smoothing_kernel(smoothing_radius, sq_distances)
            densities = np.sum(influences, axis=1)
            return densities.reshape(self.grid[0].shape)
        else:
            self._create_grid(x_size, y_size)
            grid_points = np.vstack([self.grid[0].ravel(), self.grid[1].ravel()]).T
            tree = cKDTree(self.positions)
            densities = np.zeros(grid_points.shape[0], dtype=np.float64)
            for i, point in enumerate(grid_points):
                neighbors_idx = tree.query_ball_point(point, smoothing_radius)
                if neighbors_idx:
                    distances = np.sqrt(np.sum((self.positions[neighbors_idx] - point) ** 2, axis=1))
                    influences = smoothing_kernel(smoothing_radius, distances)
                    densities[i] = np.sum(influences)

            return densities.reshape(self.grid[0].shape)

    def display_densities_heatmap(self, smoothing_radius, x_size: tuple[int, int], y_size: tuple[int, int],
                                  location: str):
        density_grid = self.calculate_densities(smoothing_radius, x_size, y_size)
        plt.figure(figsize=(10, 8))
        plt.contourf(self.grid[0], self.grid[1], density_grid, levels=40)
        plt.colorbar()
        plt.title('Density Distribution')
        plt.xlabel('X axis')
        plt.ylabel('Y axis')
        plt.tight_layout()
        if location:
            directory = location
        else:
            directory = "SPH/DensityPositions"
        # Check if the directory exists, and create it if it doesn't
        if not os.path.exists(directory):
            os.makedirs(directory)
        num_files = len([name for name in os.listdir(directory) if os.path.isfile(os.path.join(directory, name))])

        # Save the figure to the specified directory with the count + 1 in the file name
        plt.savefig(f"{directory}/density_distribution_{num_files + 1}.png")

        plt.close()


class Animate:
    def __init__(self, data_directory: str):

        if data_directory and os.path.exists(data_directory):
            files = sorted(os.listdir(data_directory), key=natural_sort_key)

            # Remove any unwanted files (like .DS_Store)
            files = [f for f in files if f.endswith(".txt") and not f.startswith('.')]

            self.PositionClasses = []

            for location in files:
                self.PositionClasses.append(
                    PositionData(data_location=os.path.join(data_directory, location), delimiters=","))
        else:
            raise ValueError("Inputted incorrect file location.")

    def animate(self, folder: str, smoothing_radius, x_size: tuple[int, int], y_size: tuple[int, int]):
        # Get the current working directory
        working_directory = os.getcwd()
        # Construct the full path to the folder within the working directory
        folder_path = os.path.join(working_directory, folder)

        # Check if the folder exists
        if not os.path.exists(folder_path):
            # If it doesn't exist, create it
            os.makedirs(folder_path)

        # Set the save location to this directory
        save_location = folder_path

        # Set up the writer object to write MP4 file
        output_mp4_path = os.path.join(save_location, "density_distributions.mp4")
        writer = imageio.get_writer(output_mp4_path, fps=20)  # You can change fps to your liking

        for Position in self.PositionClasses:
            Position.display_densities_heatmap(smoothing_radius, x_size, y_size, save_location)

        # Now, create the MP4 from the generated PNG images
        for file_name in sorted(os.listdir(save_location), key=natural_sort_key):
            if file_name.endswith('.png'):
                file_path = os.path.join(save_location, file_name)
                image = imageio.imread(file_path)
                writer.append_data(image)
                os.remove(file_path)  # Delete file after adding to mp4

        writer.close()  # Close the writer to finish writing the MP4 file
