import cv2   


image = cv2.imread('images/HP_train.jpg',cv2.IMREAD_COLOR)
#print(image)

def split_to_4_images(image):
    # load image
    img = image

    ##########################################
    # At first vertical devide image         #
    ##########################################
    # start vertical devide image
    height = img.shape[0]
    width = img.shape[1]
    # Cut the image in half
    width_cutoff = width // 2
    left1 = img[:, :width_cutoff]
    right1 = img[:, width_cutoff:]
    # finish vertical devide image

    ##########################################
    # At first Horizontal devide left1 image #
    ##########################################
    #rotate image LEFT1 to 90 CLOCKWISE
    img = cv2.rotate(left1, cv2.ROTATE_90_CLOCKWISE)
    # start vertical devide image
    height = img.shape[0]
    width = img.shape[1]
    # Cut the image in half
    width_cutoff = width // 2
    l2 = img[:, :width_cutoff]
    l1 = img[:, width_cutoff:]
    # finish vertical devide image
    #rotate image to 90 COUNTERCLOCKWISE
    l2 = cv2.rotate(l2, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #save
    #cv2.imwrite("part_left_2.jpg", l2)
    #rotate image to 90 COUNTERCLOCKWISE
    l1 = cv2.rotate(l1, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #save
    #cv2.imwrite("part_left_1.jpg", l1)

    ##########################################
    # At first Horizontal devide right1 image#
    ##########################################
    #rotate image RIGHT1 to 90 CLOCKWISE
    img = cv2.rotate(right1, cv2.ROTATE_90_CLOCKWISE)
    # start vertical devide image
    height = img.shape[0]
    width = img.shape[1]
    # Cut the image in half
    width_cutoff = width // 2
    r4 = img[:, :width_cutoff]
    r3 = img[:, width_cutoff:]
    # finish vertical devide image
    #rotate image to 90 COUNTERCLOCKWISE
    r4 = cv2.rotate(r4, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #save
    #cv2.imwrite("part_right_4.jpg", r4)
    #rotate image to 90 COUNTERCLOCKWISE
    r3 = cv2.rotate(r3, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #save
    #cv2.imwrite("part_right_3.jpg", r3)
    fourImages = [l1,l2,r3,r4]
    return fourImages


def split_to_16_images(images):
    images2 = []
    for i in range(4):
        four = split_to_4_images(images[i])
        for k in range(4):
            images2.append(four[k])
    return images2

def meanColor(image):

    average = image.mean(axis=0).mean(axis=0)
    average = np.array([average[2], average[1], average[0]])
    avg_patch = np.ones(shape = image.shape, dtype = np.uint8)*np.uint8(average)
    #print(avg_patch[0][0])
    return avg_patch[0][0]


def color_layout(image_path):
    image = cv2.imread(image_path,cv2.IMREAD_COLOR)
    mean_color_layout = []
    four_images = split_to_4_images(image)
    sixteen_image = split_to_16_images(four_images)
    for i in range(16):
        mean_color_layout.append(meanColor(sixteen_image[i]))
    return mean_color_layout

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

##it is the compare function it takes two arrays of 16 images and return true if they are similar otherwise it returns false
def is_similar_color_layout(first_array,second_array):

    sum = 0
    for i in range(16):
        if( isSimilar(first_array[i],second_array[i])):
            sum = sum+1
    if(sum>=12):
        return True
    else:
        return False
'''
#########################################################    
first_image_path = 'images/1.jpg'
second_image_path = 'images/1.jpg'
first_array = color_layout(first_image_path)
second_array = color_layout(second_image_path)
print(is_similar_color_layout(first_array,second_array))
#########################################################
'''
