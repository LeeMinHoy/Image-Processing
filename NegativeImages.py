import cv2
import matplotlib.pyplot as plt


def negative_process(img):
    height, width, _ = img.shape
    for i in range (0, height - 1):
        for j in range (0, width-1):
            pixel = img[i, j]
        
            pixel[0] = 255 - pixel[0]
            pixel[1] = 255 - pixel[1]
            pixel[2] = 255 - pixel[2]

            img[i,j] = pixel
    return img
# img = cv2.imread("./negative.png")
# negav_img = negative_process(img)
# plt.imshow(negav_img)

# #hold the window
# # plt.waitforbuttonpress()
# plt.show()
# plt.close('all')