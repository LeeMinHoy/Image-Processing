import cv2
import numpy as np

def power_law_transform(image, gamma):
    normalized_img = image / 255.0
    transformed_img = np.power(normalized_img, gamma)
    transformed_img = np.uint8(transformed_img * 255)
    return transformed_img

# image = cv2.imread('powerLaw.png', cv2.IMREAD_GRAYSCALE)

# gamma = 0.4
# output_image = power_law_transform(image, gamma)

# cv2.imshow('Original Image', image)
# cv2.imshow('Power Law Transformed Image', output_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
