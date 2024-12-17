import cv2
import matplotlib.pyplot as plt


def threshold_processing (img,threshold = 50):
    height, width, _ = img.shape

    for i in range (0, height - 1):
        for j in range (0, width-1):
            pixel = img[i, j]
            for r in range (0,3):
                if pixel[r] > threshold:
                    pixel[r] = 255
                else: 
                    pixel[r] = 0
                img[i,j] = pixel
    return img
# img = cv2.imread("./threshold.png")
# thre_img = threshold_processing(img)
# plt.imshow(thre_img, cmap='gray')
# print(thre_img)
# plt.show()

# #hold the window
# #plt.waitforbuttonpress()
# plt.close('all')