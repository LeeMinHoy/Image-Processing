import numpy as np
import cv2
import matplotlib.pyplot as plt
def to_binary (img):
    _, binary_image = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binary_image

def erosion(img,kernel_size = 3):
    heigth = img.shape[0]
    width = img.shape[1]
    pad_size = kernel_size //2
    padding_image = np.pad(img,pad_size, mode = 'constant' , constant_values= 255)

    output_img = np.zeros_like(img)

    for i in range (heigth):
        for j in range (width):
            neighbor = padding_image[i:i+kernel_size, j:j+kernel_size]
            # #for gray_scale (0-255)
            # min_value = np.min(neighbor)
            # output_img[i,j] = min_value
            
            #for binary (0-1)
            if np.all(neighbor == 255):
                output_img[i, j] = 0
            else:
                output_img[i, j] = 255
    
    return output_img

def erosion_cv2(img,kernel_size):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    output_img = cv2.erode(img,kernel,iterations = 1)
    return output_img

def dilation(img, kernel_size = 3):
    heigth = img.shape[0]
    width = img.shape[1]
    pad_size = kernel_size //2
    padding_image = np.pad(img,pad_size, mode = 'constant' , constant_values= 255)

    output_img = np.zeros_like(img)

    for i in range (heigth):
        for j in range (width):
            neighbor = padding_image[i:i+kernel_size, j:j+kernel_size]
            ##for gray_scale (0-255)
            #max_vlue = np.max(neighbor)
            #output_img[i,j] = max_value
            
            #for binary (0-1)
            if np.any(neighbor == 255):
                output_img[i, j] = 0
            else:
                output_img[i, j] = 255
    
    return output_img

def dilation_cv2(img, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    output_img = cv2.dilate(img, kernel, iterations=1)
    return output_img

def opening(img, kernel_size=3):
    eroded_img = erosion(img, kernel_size)
    opened_img = dilation(eroded_img, kernel_size)
    return opened_img

def closing(img, kernel_size=3):
    dilated_img = dilation(img, kernel_size)
    closed_img = erosion(dilated_img, kernel_size)
    return closed_img

def opening_cv2(img, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

def closing_cv2(img, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)


image = cv2.imread('dilation.png', cv2.IMREAD_GRAYSCALE)
binary_image = to_binary(image)

inverted_binary_image = cv2.bitwise_not(binary_image)

output_image = erosion(inverted_binary_image, 13)
img_cv2 = erosion_cv2(inverted_binary_image,13)

# output_image = dilation(binary_image, 13)
# img_cv2 = dilation_cv2(binary_image,13)
# edge_detect = image - img_cv2
# cv2.imshow('Erosion_CV2 Image', img_cv2)
# cv2.imshow('Erosion Image', output_image)
#cv2.imshow("edge", edge_detect)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

