import numpy as np
import cv2

def histogram_img(path):
    image = cv2.imread(path)
    histog = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    histog = cv2.normalize(histog, histog).flatten()
    return histog

def compare_hist_img(img_hist, dict_hist_imgs):      #dict_hist_imgs is a dictionary from database of images after histogram
    result={}     #"row": hist
    imgs_indx=[]
    for (row, hist) in dict_hist_imgs.items():
        d = cv2.compareHist(img_hist, hist, cv2.HISTCMP_CORREL)
        result[row] = d
    # sorting and taking the most 5 similar images
    results = sorted({(v, k) for (k, v) in result.items()}, reverse=True)[:5]
    for (d, row) in results:
        imgs_indx.append(row)
    return imgs_indx


#####test########

pic1=histogram_img('G:\pyramids.jpg')
pic2=histogram_img('G:\pyramids2.jpg')

index={
    "1":pic1,
    "2":pic2
}
#path='G:\dog.jpg'
h=histogram_img('G:\pyramids2.jpg')
#print(histogram_img(path))

c=compare_hist_img(h,index)
print(c)

