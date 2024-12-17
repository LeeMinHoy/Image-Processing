import cv2
import numpy as np
import matplotlib.pyplot as plt

def otsu_threshold_manual(image):

    hist = cv2.calcHist([image], [0], None, [256], [0, 256])
    hist = hist.ravel() / hist.sum()

    cum_sum = np.cumsum(hist)
    cum_mean = np.cumsum(hist * np.arange(256))

    max_variance = 0
    otsu_threshold = 0
    
    for t in range(1, 256):

        w0 = cum_sum[t] #cumsum = np.sum(P(i))
        w1 = 1 - w0
        
        if w0 == 0 or w1 == 0:
            continue
        
        # Tính giá trị trung bình các lớp
        mu0 = cum_mean[t] / w0   #cum_mean = np.sum(i.P(i))
        mu1 = (cum_mean[-1] - cum_mean[t]) / w1
        
        # Phương sai giữa các lớp (Tối đa hóa)
        variance = w0 * w1 * (mu0 - mu1) ** 2
        
        # Cập nhật threshold tốt nhất
        if variance > max_variance:
            max_variance = variance
            otsu_threshold = t

    return otsu_threshold

# image = cv2.imread('image.png', cv2.IMREAD_GRAYSCALE) 

# otsu_threshold = otsu_threshold_manual(image)
# print(f'Otsu Threshold: {otsu_threshold}')

# _, thresholded_image = cv2.threshold(image, otsu_threshold, 255, cv2.THRESH_BINARY)

# plt.figure(figsize=(10, 5))

# # Plot the original image
# plt.subplot(1, 2, 1)
# plt.imshow(image, cmap='gray')
# plt.title('Original Image')
# plt.axis('off')

# # Plot the thresholded image
# plt.subplot(1, 2, 2)
# plt.imshow(thresholded_image, cmap='gray')
# plt.title(f'Thresholded Image (Threshold = {otsu_threshold})')
# plt.axis('off')

# plt.show()
