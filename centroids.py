import numpy as np
from centroids_oop import Centroid

"""
Grupo 3

António Lourenço 100289
Pedro Teigão 100056
Raul Santos 112652
Tomás Quinhones 100371
"""

dir = "Science_Calibrated_Images_M57/"

# Define the positions and files
positions = {
    'black': [[90, 453]] * 12,  # Same position for all black images
    'red': [[165, 263]] * 9,    # Same position for all red images
    'green': [[127, 353]] * 12 + [[140, 320]] * 9,  # Different positions for first 12 and next 12 images
    'blue': [[101, 431]] * 11 + [[112, 407]] * 10   # Different positions for first 11 and next 10 images
}

calibrated_files = {
    'black': [f'black_M57_{i:03d}.fits' for i in range(1, 13)],
    'red': [f'red_M57_{i:03d}.fits' for i in range(1, 10)],
    'green': [f'green_M57_{i:03d}.fits' for i in range(1, 22)],
    'blue': [f'blue_M57_{i:03d}.fits' for i in range(1, 22)]
}

# Initialize the Centroid class
centroid_calculator = Centroid(dir, calibrated_files, positions)

# Get centroids for all filters
centers_2dg = centroid_calculator.get_centroids(plot=False)

# Shift and stack images for each filter
for filter_name in calibrated_files.keys():
    centroid_calculator.shift_and_stack(filter_name, plot=True)