import cv2
import matplotlib.pyplot as plt
import math
import numpy as np
def logarithmic_process(img):

    c = 255/ np.log(1+np.max(img))
    log_img = c *(np.log(1+img))
    log_img = np.array(log_img, dtype = np.uint8)
    return log_img

# #height, width, _ = img.shape

# # for i in range (0, height - 1):
# #     for j in range (0, width-1):
# #         pixel = img[i, j]
# #         for r in range (0,3):
# #             pixel[r] = 100* math.log(1+pixel[r])
# #         img[i,j] = pixel
# img = cv2.imread("./logarithmic.png")
# log_img = logarithmic_process(img)
# plt.imshow(log_img)
# #print(img)
# #hold the window
# plt.waitforbuttonpress()
# plt.close('all')