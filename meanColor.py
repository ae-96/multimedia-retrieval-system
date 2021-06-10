import cv2
import numpy as np
from matplotlib import pyplot as plt


#You will only use the 2 functions:
#    1) meanColor: to calculate the mean color of an image by passing the path of this image.
#    2) isSimilar: returns true or false indicating if there is similarity, you will pass to it the mean color of the 2 images.


#=================================Determine whether these 2 colors are similar or not======================================#
def isSimilar(meanColorQuery, meanColorStored):    
    d = []
    for i in range(0, 3):
        if meanColorQuery[i] > meanColorStored[i]:
            d.append((meanColorQuery[i] - meanColorStored[i])/meanColorQuery[i])
        else:
            d.append((meanColorStored[i] - meanColorQuery[i])/meanColorQuery[i])
    if d[0] <= 0.1 and d[1] <= 0.1 and d[2] <= 0.1:
        return True
    else:
        return False


#=====================================Calculates the mean color of the image given its path================================#
def meanColor(path):
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    average = image.mean(axis=0).mean(axis=0)
    average = np.array([average[2], average[1], average[0]])
    avg_patch = np.ones(shape = image.shape, dtype = np.uint8)*np.uint8(average)
    return avg_patch[0][0]

