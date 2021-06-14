import cv2
import numpy as np


def find_hisogram(ImagePath):
    image = cv2.imread(ImagePath, 1)
    height = image.shape[0]
    width = image.shape[1]
    channels = image.shape[2]
    # print(Image_Channels)
    histogram = np.zeros([256, channels], np.int32)

    # 0 blue, 1 green, 2 red

    for x in range(0, height):
        for y in range(0, width):
            for c in range(0, channels):
                histogram[image[x, y, c], c] += 1
    list_of_all_channels_pins=conver_histogram_to_pins(histogram)
    return list_of_all_channels_pins
    # return Histogram

def isSimilarr(bins_query,bins_db):

    normalized_db_bins=[0]*24
    normalized_query_bins=[0]*24
    for i in range(0,24):
        normalized_db_bins[i]=bins_db[i]/sum(bins_db[0:8])
        normalized_query_bins[i]=bins_query[i]/sum(bins_query[0:8])
    minimum=0
    db_pins=0
    for i in range(len(normalized_query_bins)):
        minimum+=min(normalized_query_bins[i],normalized_db_bins[i])
        db_pins+=normalized_db_bins[i]
    if (minimum/db_pins)>0.9:
        return True
    else:
        return False


def conver_histogram_to_pins(histogram):
    blue_channel_pins = [0] * 8
    green_channel_pins = [0] * 8
    red_channel_pins = [0] * 8
    pin_range=int(histogram.shape[0]/8)
    index = 0
    for i in range(0, histogram.shape[0]):
        blue_channel_pins[index] += histogram[i, 0]
        green_channel_pins[index] += histogram[i, 1]
        red_channel_pins[index] += histogram[i, 2]
        if (int((i+1)%pin_range ==0)) and (i>30):
            index+=1
    return red_channel_pins+green_channel_pins+red_channel_pins