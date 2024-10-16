import numpy as np
import scipy
import matplotlib.pyplot as plt
from astropy.io import fits
import os


"""
Grupo 3

António Lourenço 100289
Pedro Teigão 100056
Raul Santos 112652
Tomás Quinhones 100371
"""


###########

'''
Master BIAS
'''


bias_files = ["bias_cooled_2024-09-23_18-43-30_0220.fits", "bias_cooled_2024-09-23_18-43-32_0221.fits",
              "bias_cooled_2024-09-23_18-43-35_0222.fits", "bias_cooled_2024-09-23_18-43-37_0223.fits",
              "bias_cooled_2024-09-23_18-43-40_0224.fits", "bias_cooled_2024-09-23_18-43-42_0225.fits",
              "bias_cooled_2024-09-23_18-43-45_0226.fits", "bias_cooled_2024-09-23_18-43-47_0227.fits",
              "bias_cooled_2024-09-23_18-43-50_0228.fits", "bias_cooled_2024-09-23_18-43-52_0229.fits",
              "bias_cooled_2024-09-23_18-43-55_0230.fits", "bias_cooled_2024-09-23_18-43-57_0231.fits",
              "bias_cooled_2024-09-23_18-44-00_0232.fits", "bias_cooled_2024-09-23_18-44-02_0233.fits",
              "bias_cooled_2024-09-23_18-44-04_0234.fits", "bias_cooled_2024-09-23_18-44-07_0235.fits",
              "bias_cooled_2024-09-23_18-44-09_0236.fits", "bias_cooled_2024-09-23_18-44-12_0237.fits",
              "bias_cooled_2024-09-23_18-44-14_0238.fits", "bias_cooled_2024-09-23_18-44-17_0239.fits"]

# Load the Bias Images
bias_path = "23092024/BIAS/"
bias_images = []
for file in bias_files:
    image = fits.getdata(bias_path + file)
    bias_images.append(image)

# Stack the Bias images using median
master_bias = np.median(np.asarray(bias_images), axis=0)

# Create the Master Bias
savename= "23092024/M57/"+"master_bias.fits"
fits.writeto(savename, master_bias, overwrite=True)




###############

'''
Master Flat Black
'''



# Create master flat
flat_dir = "23092024/FLAT/" # Folder with all the flats
flat_files = ["flat__2024-09-23_18-52-28_black_0241.fits"]

# Load the Flat Images
flat_images = []
for file in flat_files:
    image = fits.getdata(flat_dir+file)
    flat_images.append(image)

# Stack the flat images

cflats = []
for ic in range(len(flat_images)):
    cflats.append((flat_images[ic] - master_bias)/np.median(flat_images[ic]-master_bias))
master_flat_black = np.median(cflats,axis=0)

# Save the Master Flat as a fits file

fits.writeto("23092024/M57/"+"master_flat_black.fits", master_flat_black, overwrite=True)









###############

'''
Master Flat Blue
'''



# Create master flat (Blue)
flat_dir = "23092024/FLAT/" # Folder with all the flats
flat_files = ["flat__2024-09-23_18-53-07_Blue_0242.fits", "flat__2024-09-23_18-53-47_Blue_0243.fits",
              "flat__2024-09-23_18-54-21_Blue_0244.fits", "flat__2024-09-23_18-54-43_Blue_0245.fits",
              "flat__2024-09-23_18-55-06_Blue_0246.fits", "flat__2024-09-23_18-55-29_Blue_0247.fits"]

# Load the Flat Images
flat_images = []
for file in flat_files:
    image = fits.getdata(flat_dir+file)
    flat_images.append(image)

# Stack the flat images

cflats = []
for ic in range(len(flat_images)):
    cflats.append((flat_images[ic] - master_bias)/np.median(flat_images[ic]-master_bias))
master_flat_blue = np.median(cflats,axis=0)

# Save the Master Flat as a fits file

fits.writeto("23092024/M57/"+"master_flat_blue.fits", master_flat_blue, overwrite=True)





##############

'''
Master Flat Green
'''





# Create master flat (Green)
flat_dir = "23092024/FLAT/" # Folder with all the flats
flat_files = ["flat__2024-09-23_18-56-09_Green_0248.fits", "flat__2024-09-23_18-56-31_Green_0249.fits",
              "flat__2024-09-23_18-56-54_Green_0250.fits", "flat__2024-09-23_18-57-17_Green_0251.fits",
              "flat__2024-09-23_18-57-39_Green_0252.fits"]

# Load the Flat Images
flat_images = []
for file in flat_files:
    image = fits.getdata(flat_dir+file)
    flat_images.append(image)

# Stack the flat images

cflats = []
for ic in range(len(flat_images)):
    cflats.append((flat_images[ic] - master_bias)/np.median(flat_images[ic]-master_bias))
master_flat_green = np.median(cflats,axis=0)

# Save the Master Flat as a fits file

fits.writeto("23092024/M57/"+"master_flat_green.fits", master_flat_green, overwrite=True)





#########

'''
Master Flat Red
'''



# Create master flat (Red)
flat_dir = "23092024/FLAT/" # Folder with all the flats
flat_files = ["flat__2024-09-23_18-58-24_Red_0253.fits", "flat__2024-09-23_18-58-57_Red_0254.fits",
              "flat__2024-09-23_18-59-30_Red_0255.fits", "flat__2024-09-23_19-00-02_Red_0256.fits",
              "flat__2024-09-23_19-00-35_Red_0257.fits"]

# Load the Flat Images
flat_images = []
for file in flat_files:
    image = fits.getdata(flat_dir+file)
    flat_images.append(image)

# Stack the flat images

cflats = []
for ic in range(len(flat_images)):
    cflats.append((flat_images[ic] - master_bias)/np.median(flat_images[ic]-master_bias))
master_flat_red = np.median(cflats,axis=0)

# Save the Master Flat as a fits file

fits.writeto("23092024/M57/"+"master_flat_red.fits", master_flat_red, overwrite=True)



#########

'''
Plot the Master Flat and Master Bias
'''
if __name__ == '__main__':
    plt.figure(figsize=(16, 4))

    plt.subplot(3, 2, 1)
    plt.imshow(master_bias, cmap='gray')
    plt.title('Master Bias')
    plt.colorbar()

    plt.subplot(3, 2, 2)
    plt.imshow(master_flat_black, cmap='gray')
    plt.title('Master Flat (Black)')
    plt.colorbar()

    plt.subplot(3, 2, 3)
    plt.imshow(master_flat_blue, cmap='gray')
    plt.title('Master Flat (Blue)')
    plt.colorbar()

    plt.subplot(3, 2, 4)
    plt.imshow(master_flat_green, cmap='gray')
    plt.title('Master Flat (Green)')
    plt.colorbar()

    plt.subplot(3, 2, 5)
    plt.imshow(master_flat_red, cmap='gray')
    plt.title('Master Flat (Red)')
    plt.colorbar()

    plt.tight_layout()  # Ensure proper spacing between subplots
    plt.show() 


####################################################################################################################




