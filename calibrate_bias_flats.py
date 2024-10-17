import numpy as np
import scipy
import matplotlib.pyplot as plt
from astropy.io import fits
from photutils.centroids import centroid_com, centroid_2dg
import os
from scipy.ndimage import shift

import data_reduction_oop as dr

"""
Grupo 3

António Lourenço 100289
Pedro Teigão 100056
Raul Santos 112652
Tomás Quinhones 100371
"""

# Load the Master Bias
bias_path = "M57/"
master_bias = fits.getdata(bias_path + "master_bias.fits")

# Load the Master Flat
flat_path = "M57/"
master_flat_black = fits.getdata(flat_path + "master_flat_black.fits")
master_flat_red = fits.getdata(flat_path + "master_flat_red.fits")
master_flat_green = fits.getdata(flat_path + "master_flat_green.fits")
master_flat_blue = fits.getdata(flat_path + "master_flat_blue.fits")

dir = "M57/" #Path 



def calibrate_images(dir, file_list):
    """Calibrate a list of FITS files and return calibrated images and masks."""
    denoised_images = []
    masks = []
    
    for file in file_list:
        try:
            denoised = dr.Denoise(dir, file)
            science, mask = denoised.Calibrate()
            denoised_images.append(science)
            masks.append(mask)
        except Exception as e:
            print(f"Error processing {file}: {e}")
    
    return denoised_images, masks

# Main directory path
dir = "M57/"

# Define raw file lists
raw_files = {
    "black": ['m57_2024-09-23_19-29-46_black_0323.fits',
         'm57_2024-09-23_19-32-23_black_0324.fits',
         'm57_2024-09-23_19-32-56_black_0325.fits',
         'm57_2024-09-23_19-33-29_black_0326.fits',
         'm57_2024-09-23_19-34-01_black_0327.fits',
         'm57_2024-09-23_19-34-34_black_0328.fits',
         'm57_2024-09-23_19-35-07_black_0329.fits',
         'm57_2024-09-23_19-35-39_black_0330.fits',
         'm57_2024-09-23_19-36-12_black_0331.fits',
         'm57_2024-09-23_19-36-45_black_0332.fits',
         'm57_2024-09-23_19-37-17_black_0333.fits',
         'm57_2024-09-23_19-39-29_black_0334.fits'],

    "blue": ['m57_2024-09-23_19-40-57_Blue_0335.fits',
        'm57_2024-09-23_19-42-57_Blue_0336.fits',
        'm57_2024-09-23_19-43-29_Blue_0337.fits',
        'm57_2024-09-23_19-44-02_Blue_0338.fits',
        'm57_2024-09-23_19-44-35_Blue_0339.fits',
        'm57_2024-09-23_19-45-08_Blue_0340.fits',
        'm57_2024-09-23_19-45-41_Blue_0341.fits',
        'm57_2024-09-23_19-46-13_Blue_0342.fits',
        'm57_2024-09-23_19-46-46_Blue_0343.fits',
        'm57_2024-09-23_19-47-19_Blue_0344.fits',
        'm57_2024-09-23_19-47-52_Blue_0345.fits',
        'm57_2024-09-23_19-56-47_Blue_0346.fits',
        'm57_2024-09-23_19-57-20_Blue_0347.fits',
        'm57_2024-09-23_19-57-53_Blue_0348.fits',
        'm57_2024-09-23_19-58-25_Blue_0349.fits',
        'm57_2024-09-23_19-58-58_Blue_0350.fits',
        'm57_2024-09-23_19-59-31_Blue_0351.fits',
        'm57_2024-09-23_20-00-03_Blue_0352.fits',
        'm57_2024-09-23_20-00-36_Blue_0353.fits',
        'm57_2024-09-23_20-01-09_Blue_0354.fits',
        'm57_2024-09-23_20-01-41_Blue_0355.fits'],

    "green": ['m57_2024-09-23_20-07-37_Green_0356.fits',
        'm57_2024-09-23_20-09-14_Green_0357.fits',
        'm57_2024-09-23_20-09-47_Green_0358.fits',
        'm57_2024-09-23_20-10-20_Green_0359.fits',
        'm57_2024-09-23_20-10-52_Green_0360.fits',
        'm57_2024-09-23_20-11-25_Green_0361.fits',
        'm57_2024-09-23_20-11-58_Green_0362.fits',
        'm57_2024-09-23_20-12-30_Green_0363.fits',
        'm57_2024-09-23_20-13-03_Green_0364.fits',
        'm57_2024-09-23_20-13-36_Green_0365.fits',
        'm57_2024-09-23_20-14-08_Green_0366.fits',
        'm57_2024-09-23_20-20-33_Green_0367.fits',
        'm57_2024-09-23_20-21-06_Green_0368.fits',
        'm57_2024-09-23_20-21-38_Green_0369.fits',
        'm57_2024-09-23_20-22-11_Green_0370.fits',
        'm57_2024-09-23_20-22-44_Green_0371.fits',
        'm57_2024-09-23_20-23-49_Green_0373.fits',
        'm57_2024-09-23_20-24-22_Green_0374.fits',
        'm57_2024-09-23_20-24-54_Green_0375.fits',
        'm57_2024-09-23_20-25-27_Green_0376.fits',
        'm57_2024-09-23_20-34-08_Green_0378.fits',
        'm57_2024-09-23_20-34-54_Green_0379.fits'],

    "red": ['m57_2024-09-23_20-36-16_Red_0380.fits',
        'm57_2024-09-23_20-36-49_Red_0381.fits',
        'm57_2024-09-23_20-37-54_Red_0383.fits',
        'm57_2024-09-23_20-38-27_Red_0384.fits',
        'm57_2024-09-23_20-38-59_Red_0385.fits',
        'm57_2024-09-23_20-39-32_Red_0386.fits',
        'm57_2024-09-23_20-40-05_Red_0387.fits',
        'm57_2024-09-23_20-40-38_Red_0388.fits',
        'm57_2024-09-23_20-41-10_Red_0389.fits']
}




# Process each color
calibrated_results = {}
for color, files in raw_files.items():
    calibrated_results[color] = calibrate_images(dir, files)


# Function to save calibrated images with new names
def save_calibrated_images(calibrated_images, color, output_dir):
    """Save calibrated images with new names in the specified output directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for idx, image in enumerate(calibrated_images):
        new_filename = f"{color}_M57_{idx+1:03d}.fits"  # e.g., "blackM57_001.fits"
        fits.writeto(os.path.join(output_dir, new_filename), image, overwrite=True)
        print(f"Saved {new_filename} in {output_dir}")

# Define output directory
output_dir = "Science_Calibrated_Images_M57/"

# Process and save for each color
for color, files in raw_files.items():
    calibrated_images, masks = calibrate_images(dir, files)
    if calibrated_images:  # Check if there are calibrated images to save
        save_calibrated_images(calibrated_images, color, output_dir)


# Warning: The file 'm57_2024-09-23_20-37-21_Red_0382.fits' has an error so it was removed
# Warning: The old file 'red_M57_002.fits' has an error so it was removed 
# Warning: The file 'm57_2024-09-23_20-23-16_Green_0372.fits' has an error so it was removed
# Warning: The old file 'green_M57_019.fits' has an error so it was removed
# Warning: The file 'm57_2024-09-23_20-33-26_Green_0377.fits' has an error so it was removed
# Warning: The old file 'green_M57_022.fits' has an error so it was removed

# Tests


# Black
color = "black"
if calibrated_results[color][0]:  # Check if there's at least one calibrated image
    lo, up = np.percentile(calibrated_results[color][0][0], (5, 95))
    plt.imshow(calibrated_results[color][0][0], cmap='gray', vmin=lo, vmax=up)
    plt.title(f'Denoised Image - {color.capitalize()}')
    plt.colorbar()
    plt.show()

# Blue
color = "blue"
if calibrated_results[color][0]:  # Check if there's at least one calibrated image
    lo, up = np.percentile(calibrated_results[color][0][0], (5, 95))
    plt.imshow(calibrated_results[color][0][0], cmap='gray', vmin=lo, vmax=up)
    plt.title(f'Denoised Image - {color.capitalize()}')
    plt.colorbar()
    plt.show()

# Green
color = "green"
if calibrated_results[color][0]:  # Check if there's at least one calibrated image
    lo, up = np.percentile(calibrated_results[color][0][0], (5, 95))
    plt.imshow(calibrated_results[color][0][0], cmap='gray', vmin=lo, vmax=up)
    plt.title(f'Denoised Image - {color.capitalize()}')
    plt.colorbar()
    plt.show()

# Red
color = "red"
if calibrated_results[color][0]:  # Check if there's at least one calibrated image
    lo, up = np.percentile(calibrated_results[color][0][0], (5, 95))
    plt.imshow(calibrated_results[color][0][0], cmap='gray', vmin=lo, vmax=up)
    plt.title(f'Denoised Image - {color.capitalize()}')
    plt.colorbar()
    plt.show()





