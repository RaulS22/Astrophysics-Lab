import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from photutils.centroids import centroid_2dg
from scipy.ndimage import shift
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
        self.data_all = {}
        self.centers_2dg = {}

        # Load all FITS files and store in data_all
        for filter_name, files in calibrated_files.items():
            self.data_all[filter_name] = []
            for filename in files:
                data = fits.getdata(os.path.join(dir, filename))
                self.data_all[filter_name].append(data)

    def get_centroids(self, plot=False):
        for filter_name in self.calibrated_files.keys():
            self.centers_2dg[filter_name] = []  # To store centers for each filter
            for i, (data, pos) in enumerate(zip(self.data_all[filter_name], self.positions[filter_name])):
                # Extract the sub-image (60x60) around the specified position
                subdata = data[pos[1]-30:pos[1]+30, pos[0]-30:pos[0]+30]
                center_2dg = centroid_2dg(subdata)  # Centroid within the 60x60 sub-image

                # Adjust to the full image coordinates
                center_2dg_full = center_2dg + np.array(pos) - [30, 30]
                self.centers_2dg[filter_name].append(center_2dg_full)

                # Optional plotting
                if plot:
                    plt.imshow(subdata, origin='lower', cmap='gray')
                    plt.plot(center_2dg[0], center_2dg[1], 'r+', markersize=10, label='Centroid')
                    plt.show()

        return self.centers_2dg

    def shift_and_stack(self, filter_name, plot=False):
        output_dir = os.path.join(self.dir, "Stacked_Images_M57/")
        os.makedirs(output_dir, exist_ok=True)

        centers = self.centers_2dg[filter_name]
        data = self.data_all[filter_name]
        
        reference_center = centers[0]  # Use the first image's center as the reference
        shifted_images = []  # To store shifted images
        
        mask_y1 = 0
        mask_x1 = 0
        mask_y2 = 0
        mask_x2 = 0

        # Shift images
        for i, (img, center) in enumerate(zip(data, centers)):
            shift_y = -int(np.round(center[1] - reference_center[1]))
            shift_x = -int(np.round(center[0] - reference_center[0]))

            # Update masks for out-of-bounds areas
            mask_y1 = min(mask_y1, shift_y)
            mask_x1 = min(mask_x1, shift_x)
            mask_y2 = max(mask_y2, shift_y)
            mask_x2 = max(mask_x2, shift_x)

            # Shift the image
            shifted_img = shift(img, (shift_y, shift_x), mode='constant', cval=0.0)
            shifted_images.append(shifted_img)

        # Stack shifted images by summing them
        combined_image = np.sum(shifted_images, axis=0)

        # Set out-of-bounds pixels to 0
        h, w = combined_image.shape
        combined_image[:mask_y2, :] = 0
        combined_image[h + mask_y1 + 1:, :] = 0
        combined_image[:, :mask_x2] = 0
        combined_image[:, w + mask_x1 + 1:] = 0

        # Save the combined image as a FITS file
        filename = os.path.join(output_dir, f"stacked_{filter_name}.fits")
        fits.writeto(filename, combined_image, overwrite=True)
        print(f"Saved: {filename}")

        # Optional plot
        if plot:
            lo, up = np.percentile(combined_image, 5), np.percentile(combined_image, 95)
            plt.imshow(combined_image, cmap='gray', clim=(lo, up))
            plt.colorbar()
            plt.title(f"Stacked {filter_name.capitalize()} Image")
            plt.xlabel('xpix')
            plt.ylabel('ypix')
            plt.show()

        return combined_image
