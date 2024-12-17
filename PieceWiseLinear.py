import cv2
import matplotlib.pyplot as plt

def piecewiseLinear(img,r1,s1,r2,s2):
    height, width, _ = img.shape
    for i in range (0, height - 1):
        for j in range (0, width-1):
            pixel = img[i,j]
            for k in range (0,3):
                r = pixel[k]
                if r <= r1:
                    pixel[k] = (s1/r1)*r
                elif r1 < r<= r2:
                    pixel[k] = ((s2 - s1) / (r2-r1))*(r-r1)+s1
                else:
                    pixel[k] = ((255-s2)/(255-r2))*(r-r2) +s2 
    return img

# img = cv2.imread("./pieceWise2.png")
# # r: Input gray level
# # s: Output gray level
# r1,s1 = 90,40
# r2,s2 = 180,220
# pieceImg = piecewiseLinear(img,r1,s1,r2,s2 )

# print(pieceImg)

# plt.imshow(pieceImg)

# #hold the window
# plt.waitforbuttonpress()
# plt.close('all')