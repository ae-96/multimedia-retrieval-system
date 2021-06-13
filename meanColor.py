import cv2
import numpy as np
from matplotlib import pyplot as plt


#You will only use the 2 functions:
#    1) meanColor: to calculate the mean color of an image by passing the path of this image.
#    2) isSimilar: returns true or false indicating if there is similarity, you will pass to it the mean color of the 2 images.


#=================================Calculates the distance between the mean color of 2 images===============================#   
def isSimilar(meanColorQuery, meanColorStored):    
    minRange = [0, 0, 0]
    maxRange = [0, 0, 0]
    for i in range(0, 3):
        if meanColorStored[i] < 26:
            minRange[i] = 0
        else:
            minRange[i] = meanColorStored[i] - 26
        
        if meanColorStored[i] > 229:
            maxRange[i] = 255
        else:
            maxRange[i] = meanColorStored[i] + 26
        
    for i in range(0, 3):
        if not(meanColorQuery[i] <= maxRange[i] and meanColorQuery[i] >= minRange[i]):
            return False
    
    return True

#=====================================Calculates the mean color of the image given its path================================#
def meanColor(path):
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    average = image.mean(axis=0).mean(axis=0)
    average = np.array([average[2], average[1], average[0]])
    avg_patch = np.ones(shape = image.shape, dtype = np.uint8)*np.uint8(average)
    return avg_patch[0][0]

