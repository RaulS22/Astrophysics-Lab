import numpy as np
import scipy
import matplotlib.pyplot as plt
from astropy.io import fits
from photutils.centroids import centroid_com, centroid_2dg

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
bias_path = "23092024/BIAS/"
master_bias = fits.getdata(bias_path + "master_bias.fits")

# Load the Master Flat
flat_path = "23092024/FLAT/"
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
    








# Now, we'll create the class to deal with the shifting of the images
# We'll calculate the centroid and make use of it to shift the images accordingly

class Centroid():

    def __init__(self, dir, file1, file2, pos1, pos2):
        '''
        This class will be used to shift the images
        
        Parameters:
        dir: str
            The path to the files
        
        file1: str
            The first file name

        file2: str
            The second file name

        pos1: ndarray
            The rough position of the centroid of the 1st image

        pos2: ndaray
            The rough position of the centroid of the 2nd image
        '''

        self.dir = dir
        self.file1 = file1
        self.file2 = file2
        self.pos1 = pos1
        self.pos2 = pos2

        # Testing
        if isinstance(dir, str) == False:
            raise ValueError("Path must be a string")
        
        if isinstance(file1, str) == False:
            raise ValueError("File1 must be a string")
        
        if isinstance(file2, str) == False:
            raise ValueError("File2 must be a string")
        
    def get_centroids(self, plot=False):
            '''
            Get a subdata of 60x60 pixels around the centroid images

            Parameters:
            plot: bool
                If True, it will plot the subdata of the images
            '''
            data1 = fits.getdata(self.dir + self.file1)
            data2 = fits.getdata(self.dir + self.file2)
            pos1 = np.array(self.pos1)
            pos2 = np.array(self.pos2)

            subdata1 = data1[pos1[1]-30:pos1[1]+30, pos1[0]-30:pos1[0]+30]
            subdata2 = data2[pos2[1]-30:pos2[1]+30, pos2[0]-30:pos2[0]+30]

            center1,center2 = centroid_2dg(subdata1)+pos1-[30,30],centroid_2dg(subdata2)+pos2-[30,30]
            c_center1,c_center2 = centroid_com(subdata1)+pos1-[30,30],centroid_com(subdata2)+pos2-[30,30]

            if plot == True:
            
                plt.imshow(subdata1)
                plt.plot(centroid_2dg(subdata1)[0], centroid_2dg(subdata1)[1], 'r+', markersize=10, label='Centroid')
                plt.plot(centroid_com(subdata1)[0], centroid_com(subdata1)[1], 'w+', markersize=10, label='Centroid COM')
                plt.title('Subdata 1')
                plt.colorbar()
                plt.show()

                plt.imshow(subdata2)
                plt.plot(centroid_2dg(subdata2)[0], centroid_2dg(subdata2)[1], 'r+', markersize=10, label='Centroid')
                plt.plot(centroid_com(subdata2)[0], centroid_com(subdata2)[1], 'w+', markersize=10, label='Centroid COM')
                plt.title('Subdata 2')
                plt.colorbar()
                plt.show()

            return center1,center2,c_center1,c_center2
        
            

        








 
    
# Testing the Denoise class
if __name__ == "__main__":
    file1 = 'm57_2024-09-23_19-29-46_black_0323.fits'
    file2 = 'm57_2024-09-23_19-32-23_black_0324.fits'
    file3 = 'm57_2024-09-23_19-32-56_black_0325.fits'
    path = '23092024/M57/'

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

    path = '23092024/'
    fits.writeto(path + 'calibrated_' + file1, science_1, overwrite=True)
    fits.writeto(path + 'calibrated_' + file2, science_2, overwrite=True)
    fits.writeto(path + 'calibrated_' + file3, science_3, overwrite=True)



# Testing the Centroid class
if __name__ == "__main__":
    file1 = 'calibrated_m57_2024-09-23_19-29-46_black_0323.fits'
    file2 = 'calibrated_m57_2024-09-23_19-32-23_black_0324.fits'
    file3 = 'calibrated_m57_2024-09-23_19-32-56_black_0325.fits'

    dir = '23092024/'

    pos1 = [610, 739]
    pos2 = [611, 726]
    pos3 = [612, 718]

    centroid = Centroid(dir, file1, file2, pos1, pos2)
    center1, center2, c_center1, c_center2 = centroid.get_centroids(plot=True)
    print(center1, center2, c_center1, c_center2)

    centroid = Centroid(dir, file1, file3, pos1, pos3)
    center1, center3, c_center1, c_center3 = centroid.get_centroids(plot=True)
    print(center1, center3, c_center1, c_center3)

    
