import numpy as np
import matplotlib.pyplot as plt
import cv2
def bit_plane_slicing(img,bit_plane):    
    bit_plane_image = np.zeros_like(img)
    height, width, _ = img.shape
    for i in range (0, height - 1):
        for j in range (0, width-1):
            for k in range (0,3):
                bit_value = (img[i, j][k] >> bit_plane) & 1
                bit_plane_image[i, j][k] = bit_value * 255

    return bit_plane_image


# # Hàm hiển thị các bit plane
# def display_bit_planes(image):
#     # Tạo một figure để hiển thị các bit plane
#     plt.figure(figsize=(12, 8))
    
#     for i in range(8):
#         # Lấy ảnh của bit plane thứ 'bit_plane'
#         bit_plane_image = bit_plane_slicing(image,i)
        
#         # Hiển thị ảnh bit plane
#         plt.subplot(2, 4, i + 1)
#         plt.imshow(bit_plane_image, cmap='gray')
#         plt.title(f'Bit Plane {i}')
#         plt.axis('off')
    
#     plt.show()

# img = cv2.imread("./bitplaneslicing.png")
# display_bit_planes(img)
