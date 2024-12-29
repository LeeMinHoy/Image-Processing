import numpy as np
import cv2
import matplotlib.pyplot as plt

def ideal_low_pass_filter(image_shape, cutoff):
    P, Q = image_shape
    H = np.zeros((P, Q))
    center = (P // 2, Q // 2)

    for u in range(P):
        for v in range(Q):
            D = np.sqrt((u - center[0]) ** 2 + (v - center[1]) ** 2)
            if D <= cutoff:
                H[u, v] = 1
            else: H[u,v] = 0
    return H

def butterworth_low_pass_filter(image_shape, cutoff, order):
    P, Q = image_shape
    H = np.zeros((P, Q))
    center = (P // 2, Q // 2)

    for u in range(P):
        for v in range(Q):
            D = np.sqrt((u - center[0]) ** 2 + (v - center[1]) ** 2)
            H[u, v] = 1 / (1 + (D / cutoff) ** (2 * order))
    return H

def gaussian_low_pass_filter(image_shape, cutoff):
    P, Q = image_shape
    H = np.zeros((P, Q))
    center = (P // 2, Q // 2)

    for u in range(P):
        for v in range(Q):
            D = np.sqrt((u - center[0]) ** 2 + (v - center[1]) ** 2)
            H[u, v] = np.exp(-(D ** 2) / (2 * (cutoff ** 2)))
    return H


def apply_filter_in_frequency_domain(image, filter_mask):
    # FFT and shift
    dft = np.fft.fft2(image)
    dft_shift = np.fft.fftshift(dft)

    # Apply the filter
    filtered_dft = dft_shift * filter_mask

    # Inverse FFT
    dft_inverse_shift = np.fft.ifftshift(filtered_dft)
    image_filtered = np.fft.ifft2(dft_inverse_shift)
    image_filtered = np.abs(image_filtered)

    return image_filtered

# def plot_results(original_image, filtered_images, filter_names):
#     plt.figure(figsize=(15, 8))
#     plt.subplot(2, 3, 1)
#     plt.imshow(original_image, cmap='gray')
#     plt.title("Original Image")
#     plt.axis('off')

#     for i, (filtered_image, name) in enumerate(zip(filtered_images, filter_names), start=2):
#         plt.subplot(2, 3, i)
#         plt.imshow(filtered_image, cmap='gray')
#         plt.title(name)
#         plt.axis('off')

#     plt.tight_layout()
#     plt.show()

# # Load image
# gray_image = cv2.imread('gaussian.png', cv2.IMREAD_GRAYSCALE)

# # Image shape for filter generation
# image_shape = gray_image.shape

# # Generate filters
# cutoff_frequency = 50
# order = 2

# #ideal_filter = ideal_low_pass_filter(image_shape, cutoff_frequency)
# #butterworth_filter = butterworth_low_pass_filter(image_shape, cutoff_frequency, order)
# gaussian_filter = gaussian_low_pass_filter(image_shape, cutoff_frequency)

# # Apply filters
# #ideal_filtered_image = apply_filter_in_frequency_domain(gray_image, ideal_filter)
# #butterworth_filtered_image = apply_filter_in_frequency_domain(gray_image, butterworth_filter)
# gaussian_filtered_image = apply_filter_in_frequency_domain(gray_image, gaussian_filter)

# # Plot results
# plot_results(gray_image, [gaussian_filtered_image],
#              ["Gaussian Low-Pass Filter"])
