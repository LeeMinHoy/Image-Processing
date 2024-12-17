import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load the image in grayscale
image_path = 'otsu.png'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Apply Otsu's thresholding
_, otsu_threshold = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Display the results
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.title('Original Image')
plt.imshow(image, cmap='gray')

plt.subplot(1, 2, 2)
plt.title(f'Otsu Threshold (T={_: .2f})')
plt.imshow(otsu_threshold, cmap='gray')
plt.show()
