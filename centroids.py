import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from photutils.centroids import centroid_2dg
import os

"""
Grupo 3

António Lourenço 100289
Pedro Teigão 100056
Raul Santos 112652
Tomás Quinhones 100371
"""


class Centroid:
    def __init__(self, dir, calibrated_files, positions):
        self.dir = dir
        self.calibrated_files = calibrated_files
        self.positions = positions

        if not isinstance(dir, str):
            raise ValueError("Path must be a string")
        
        if not isinstance(calibrated_files, dict):
            raise ValueError("Calibrated files must be a dictionary")
        
        if not isinstance(positions, dict):
            raise ValueError("Positions must be a dictionary")
        
        self.data_all = self.load_data()

    def load_data(self):
        """Load FITS images for each filter into a dictionary."""
        data_all = {}
        for filter_name, files in self.calibrated_files.items():
            data_all[filter_name] = []
            for filename in files:
                filepath = os.path.join(self.dir, filename)
                data = fits.getdata(filepath)
                data_all[filter_name].append(data)
        return data_all

    def get_centroids(self, plot=False):
        """Calculate centroids for all filters."""
        centroids = {}

        for filter_name in self.calibrated_files.keys():
            filter_centroids = []  # To store centers for each filter

            for i, (data, pos) in enumerate(zip(self.data_all[filter_name], self.positions[filter_name])):
                # Extract the sub-image (60x60) around the specified position
                subdata = data[pos[1] - 30:pos[1] + 30, pos[0] - 30:pos[0] + 30]

                # Calculate the centroid within the 60x60 sub-image
                centroid = centroid_2dg(subdata)
                centroid_full = centroid + np.array(pos) - [30, 30]  # Adjust for full image coordinates

                filter_centroids.append(centroid_full)

                if plot:
                    self.plot_subdata(subdata, centroid)

                # Print centroid for each image
                print(f"{filter_name.capitalize()} Image {i+1} - 2D Gaussian Center (full image coordinates): {centroid_full}")

            centroids[filter_name] = filter_centroids

        return centroids

    def plot_subdata(self, subdata, centroid):
        """Plot the sub-image with the calculated centroid."""
        plt.imshow(subdata, origin='lower', cmap='gray')
        plt.plot(centroid[0], centroid[1], 'r+', markersize=10, label='Centroid')
        plt.title('Subdata with Centroid')
        plt.colorbar()
        plt.legend()
        plt.show()


# Example usage:
if __name__ == '__main__':
    dir_path = "Science_Calibrated_Images_M57/"
    
    # File structure organized by filter
    calibrated_files = {
        'black': [
            'black_M57_001.fits', 'black_M57_002.fits', 'black_M57_003.fits',
            'black_M57_004.fits', 'black_M57_005.fits', 'black_M57_006.fits',
            'black_M57_007.fits', 'black_M57_008.fits', 'black_M57_009.fits',
            'black_M57_010.fits', 'black_M57_011.fits', 'black_M57_012.fits'
        ],
        'red': [
            'red_M57_001.fits', 'red_M57_002.fits', 'red_M57_003.fits',
            'red_M57_004.fits', 'red_M57_005.fits', 'red_M57_006.fits',
            'red_M57_007.fits', 'red_M57_008.fits', 'red_M57_009.fits'
        ],
        'green': [
            'green_M57_001.fits', 'green_M57_002.fits', 'green_M57_003.fits',
            'green_M57_004.fits', 'green_M57_005.fits', 'green_M57_006.fits',
            'green_M57_007.fits', 'green_M57_008.fits', 'green_M57_009.fits',
            'green_M57_010.fits', 'green_M57_011.fits', 'green_M57_012.fits',
            'green_M57_013.fits', 'green_M57_014.fits', 'green_M57_015.fits',
            'green_M57_016.fits', 'green_M57_017.fits', 'green_M57_018.fits',
            'green_M57_019.fits', 'green_M57_020.fits', 'green_M57_021.fits',
            'green_M57_022.fits', 'green_M57_023.fits', 'green_M57_024.fits'
        ],
        'blue': [
            'blue_M57_001.fits', 'blue_M57_002.fits', 'blue_M57_003.fits',
            'blue_M57_004.fits', 'blue_M57_005.fits', 'blue_M57_006.fits',
            'blue_M57_007.fits', 'blue_M57_008.fits', 'blue_M57_009.fits',
            'blue_M57_010.fits', 'blue_M57_011.fits', 'blue_M57_012.fits',
            'blue_M57_013.fits', 'blue_M57_014.fits', 'blue_M57_015.fits',
            'blue_M57_016.fits', 'blue_M57_017.fits', 'blue_M57_018.fits',
            'blue_M57_019.fits', 'blue_M57_020.fits', 'blue_M57_021.fits'
        ]
    }
    
    # Define positions for each filter
    positions = {
        'black': [[90, 453]] * 12,
        'red': [[165, 263]] * 8 + [[150, 260]] * 1,
        'green': [[140, 353]] * 12 + [[140, 320]] * 12,
        'blue': [[101, 431]] * 11 + [[112, 407]] * 10
    }
    
    # Create the Centroid object
    centroid_calculator = Centroid(dir_path, calibrated_files, positions)
    
    # Get and plot centroids for each filter
    centroids = centroid_calculator.get_centroids(plot=True)
