import numpy as np
import scipy
import matplotlib.pyplot as plt
from astropy.io import fits

"""
Grupo 3

António Lourenço 100289
Pedro Teigão 100056
Raul Santos 112652
Tomás Quinhones 100371
"""

# We'll deal with the data using oriented Object-oriented Programming

# First, we'll create the master bias and master flat
# OOP wasn't required for this part, just functional programming
# Since it has been done before, we'll just load them


# Load the Master Bias
bias_path = "M57/"
master_bias = fits.getdata(bias_path + "master_bias.fits")

# Load the Master Flat
flat_path = "M57/"
master_flat_black = fits.getdata(flat_path + "master_flat_black.fits")
master_flat_red = fits.getdata(flat_path + "master_flat_red.fits")
master_flat_green = fits.getdata(flat_path + "master_flat_green.fits")
master_flat_blue = fits.getdata(flat_path + "master_flat_blue.fits")


# Now, we'll create the class to deal with the denoising of the images
class Denoise():

    def __init__(self, path, file, bias=master_bias, flat=master_flat_black):
        '''
        This class will be used to denoise the images' noise
        
        Parameters:
        path: str
            The path to the file

        file: str
            The file name

        bias: .fits file
            The master bias

        flat: .fits file
            The master flat, if not provided, it will be the black master flat

        Returns:
        science: .fits file
            The science image with the noise removed

        mask: .fits file
            The mask of the science image

        
        '''

        
        self.path = path
        self.file = file
        self.bias = bias
        self.flat = flat


    # Testing
        if isinstance(path, str) == False:
            raise ValueError("Path must be a string")

    def science_image(self):
        '''
        Get the science image
        '''
        science = fits.getdata(self.path + self.file)
        return science
    
    def Calibrate(self):
        '''
        Calibrate the science file with the master bias and master flat
        '''
        science = self.science_image()
        science_calibrated = (science - self.bias) / self.flat

        mask=np.zeros(np.shape(science_calibrated))
        for i in range(len(science_calibrated)):
            for j in range(len(science_calibrated[i])):
                if self.flat[i][j]<0.2:
                    science_calibrated[i][j]=0
                    mask[i][j]=1
        mask=mask.astype(bool)

        return science_calibrated, mask
            
            

        








""" 
    
# Testing the Denoise class
if __name__ == "__main__":
    file1 = 'm57_2024-09-23_19-29-46_black_0323.fits'
    file2 = 'm57_2024-09-23_19-32-23_black_0324.fits'
    file3 = 'm57_2024-09-23_19-32-56_black_0325.fits'
    path = 'M57/'

    denoised_1 = Denoise(path, file1)
    science_1, mask_1 = denoised_1.Calibrate()
    lo, up = np.percentile(science_1, (5, 95))

    #plt.figure(figsize=(10,10))
    #plt.imshow(science_1, cmap='gray', vmin=lo, vmax=up)
    #plt.title('Denoised Image 1')
    #plt.colorbar()
    #plt.show()


    denoised_2 = Denoise(path, file2)
    science_2, mask_2 = denoised_2.Calibrate()
    lo, up = np.percentile(science_2, (5, 95))

    #print(science_1)
    #print(science_2)

    #plt.figure(figsize=(10,10))
    #plt.imshow(science_2, cmap='gray', vmin=lo, vmax=up)
    #plt.title('Denoised Image 2')
    #plt.colorbar()
    #plt.show()

    denoised_3 = Denoise(path, file3)
    science_3, mask_3 = denoised_3.Calibrate()
    lo, up = np.percentile(science_3, (5, 95))

    path = ''
    fits.writeto(path + 'calibrated_' + file1, science_1, overwrite=True)
    fits.writeto(path + 'calibrated_' + file2, science_2, overwrite=True)
    fits.writeto(path + 'calibrated_' + file3, science_3, overwrite=True)

"""

