import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from photutils.centroids import centroid_2dg
import os

class Centroid:
    def __init__(self, dir, calibrated_files, positions):
        '''
        This class will be used to calculate centroids for multiple images.

        Parameters:
        dir: str
            The path to the files
        
        calibrated_files: list
            List of FITS file names
        
        positions: list of ndarray
            List of rough positions for the centroids of each image
        '''
        self.dir = dir
        self.calibrated_files = calibrated_files
        self.positions = positions

        # Validate inputs
        if not isinstance(dir, str):
            raise ValueError("Path must be a string")
        
        if not isinstance(calibrated_files, list):
            raise ValueError("Calibrated files must be a list")
        
        if not isinstance(positions, list):
            raise ValueError("Positions must be a list")
        
    def get_centroids(self, plot=False):
        '''
        Calculate the centroids for all images and optionally plot the results.

        Parameters:
        plot: bool
            If True, plots the subdata and centroids for each image.
        
        Returns:
        centroids: list
            List of centroids for all images.
        '''
        centroids = []

        for file, pos in zip(self.calibrated_files, self.positions):
            data = fits.getdata(os.path.join(self.dir, file))
            pos = np.array(pos)

            # Extract a subimage around the rough centroid position
            subdata = data[pos[1]-30:pos[1]+30, pos[0]-30:pos[0]+30]

            # Calculate centroids
            centroid = centroid_2dg(subdata) + pos - np.array([30, 30])
            centroids.append(centroid)

            if plot:
                self.plot_subdata(subdata, centroid)

        return centroids

    def plot_subdata(self, subdata, centroid):
        '''
        Helper function to plot the subdata and its centroid.

        Parameters:
        subdata: ndarray
            The extracted subimage data.
        
        centroid: ndarray
            The calculated centroid position.
        '''
        plt.imshow(subdata, origin='lower', cmap='gray')
        plt.plot(centroid[0]-30, centroid[1]-30, 'r+', markersize=10, label='Centroid')
        plt.title('Subdata with Centroid')
        plt.colorbar()
        plt.legend()
        plt.show()

if __name__ == '__main__':
    dir_path = "Science_Calibrated_Images_M57/"
    positions = [
    
    ]

    calibrated_files = [
    
    ]

    centroid_calculator = Centroid(dir_path, calibrated_files, positions)
    centroids = centroid_calculator.get_centroids(plot=True)
