# Astrophysics-Lab


# Acknowledgements
This repository has been created to present our results on the "Astrphysics Laboratory" 
Course at Instituto Superior Tecnico. We would like to thank professor Ana Maria Cidade Mourão
and João Ricardo Dias Duarte for the help at the experimental part and the suport with the code.

# M57

We observed the Ring Nebula M57 at the night of September 19th and the data colected is presented
on the folder "/M57". The file "bias_and_flats.py" creates a "master_bias" fit and the "master_flat" fit for each filter. Functional programing was used in both of this codes since there was a simple procedure.

The file "calibrate_bias_flats.py" normalize the illumination of each image, this code also renames each image in a easier way to process in a workflow and saves them in the folder "/Science_Calibrated_Images_M57". Object-Oriented Programing (OOP) was used here to simplify some procedures. Finally, the file "centroids.py" comes in hand in order to align and to stack the images. It also uses OOP. The classes and instances are in different files "data_reduction_oop.py" and "centroids_oop.py", respectively.

The apperture and surface photometry were performed used Jupyter Notebooks. These files are present in the "/Photometry" folder.


# Sheliak

For Sheliak it was also choosen to use Jupyter Notebooks. All files are in the folder "/Sheliak".

# Group

António Lourenço    - 100289
Pedro Teigão        - 100056
Raul Santos         - 112652
Tomás Quinhones     - 100371