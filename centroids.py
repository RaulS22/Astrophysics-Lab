import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from photutils.centroids import centroid_2dg
import os

from centroids_oop import Centroid


# Directory path
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

# Rough positions for each filter
positions = {
    'black': [[90, 483]] * len(calibrated_files['black']),  # Same position for all black files
    'red': [[150, 275]] * len(calibrated_files['red']),     # Same position for all red files
    'green': [[145, 280]] * len(calibrated_files['green']), # Same position for all green files
    'blue': [[100, 435]] * 12 + [[120, 420]] * 9            # First 12 blue files have pos_B1, the rest pos_B2
}

# Create an instance of the Centroid class and calculate centroids
centroid_calculator = Centroid(dir_path, calibrated_files, positions)
centroids = centroid_calculator.get_centroids(plot=True)