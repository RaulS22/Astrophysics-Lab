import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from photutils.centroids import centroid_2dg
import os

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

    def get_centroids(self, plot=False):
        centroids = {}
        
        for filter_name, files in self.calibrated_files.items():
            filter_centroids = []

            # Get the reference file's position and data
            ref_file = files[0]
            ref_pos = self.positions[filter_name][0]

            # Load the reference image
            ref_data = fits.getdata(os.path.join(self.dir, ref_file))
            ref_subdata = ref_data[ref_pos[1]-40:ref_pos[1]+40, ref_pos[0]-40:ref_pos[0]+40]
        
            # Calculate centroid for the reference image
            ref_centroid = centroid_2dg(ref_subdata) + ref_pos - np.array([40, 40])
            filter_centroids.append(ref_centroid)

            for file, pos in zip(files, self.positions[filter_name]):
                data = fits.getdata(os.path.join(self.dir, file))
                pos = np.array(pos)

                subdata = data[pos[1]-30:pos[1]+30, pos[0]-30:pos[0]+30]
                centroid = centroid_2dg(subdata) + pos - np.array([30, 30])
                
                # Calculate shift from reference centroid
                shifted_centroid = centroid - ref_centroid
                filter_centroids.append(shifted_centroid)

                if plot:
                    self.plot_subdata(subdata, centroid)

            centroids[filter_name] = filter_centroids

        return centroids

    def plot_subdata(self, subdata, centroid):
        plt.imshow(subdata, origin='lower', cmap='gray')
        plt.plot(centroid[0]-30, centroid[1]-30, 'r+', markersize=10, label='Centroid')
        plt.title('Subdata with Centroid')
        plt.colorbar()
        plt.legend()
        plt.show()


"""
if __name__ == '__main__':
    dir_path = "Science_Calibrated_Images_M57/"
    
"""