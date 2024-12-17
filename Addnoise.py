import numpy as np
import cv2

def add_gaussian_noise(image, mean=0, sigma=25):
    gaussian = np.random.normal(mean, sigma, image.shape).astype(np.float32)
    noisy_image = image.astype(np.float32) + gaussian
    noisy_image = np.clip(noisy_image, 0, 255) 
    return noisy_image.astype(np.uint8)

def add_uniform_noise(image, low=-50, high=50):
    uniform = np.random.uniform(low, high, image.shape).astype(np.float32)
    noisy_image = image.astype(np.float32) + uniform
    noisy_image = np.clip(noisy_image, 0, 255)
    return noisy_image.astype(np.uint8)

def add_salt_pepper_noise(image, salt_prob=0.01, pepper_prob=0.01):
    noisy_image = image.copy()
    total_pixels = image.size

    # Add salt noise
    num_salt = int(salt_prob * total_pixels)
    salt_coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape]
    noisy_image[salt_coords[0], salt_coords[1]] = 255

    # Add pepper noise
    num_pepper = int(pepper_prob * total_pixels)
    pepper_coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape]
    noisy_image[pepper_coords[0], pepper_coords[1]] = 0

    return noisy_image

image = cv2.imread('bitplaneslicing.png')

gaussian_noisy_image = add_gaussian_noise(image)
uniform_noisy_image = add_uniform_noise(image)
salt_pepper_noisy_image = add_salt_pepper_noise(image)

#cv2.imshow('gaussian_noisy_image.jpg', gaussian_noisy_image)
#cv2.imshow('uniform_noisy_image.jpg', uniform_noisy_image)
cv2.imwrite('salt_pepper_noisy_image.jpg', salt_pepper_noisy_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
