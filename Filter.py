import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
def load_image(image_path):
    image = cv2.imread(image_path)
    return image

def mean_filter(image, size=3):
    return cv2.blur(image, (size, size))

def median_filter(image,size = 3):
    return cv2.medianBlur(image, size)

def normalized_correlation(image, template):
    # Kích thước của template
    h, w = template.shape

    # Thực hiện template matching với normalized cross-correlation
    result = cv2.matchTemplate(image, template, cv2.TM_CCORR_NORMED)

    # Tìm vị trí tốt nhất
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # Vẽ hình chữ nhật tại vị trí tốt nhất
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    image_with_rectangle = image.copy()  # Tạo bản sao để không ghi đè ảnh gốc
    cv2.rectangle(image_with_rectangle, top_left, bottom_right, 255, 2)

    print(f"Max correlation value: {max_val:.4f}")
    print(f"Top-left corner of match: {top_left}")

    return image_with_rectangle


def normalized_correlation_manual(image, template):
    # Kích thước của image và template
    img_height, img_width = image.shape
    template_height, template_width = template.shape
    
    # Tạo ma trận kết quả cho việc lưu giá trị tương tự
    result = np.zeros((img_height - template_height + 1, img_width - template_width + 1))

    # Tính toán trung bình của template
    mean_template = np.mean(template)

    # Duyệt qua từng pixel của hình ảnh
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            # Lấy vùng cửa sổ từ hình ảnh có cùng kích thước với template
            window = image[i:i + template_height, j:j + template_width]

            # Tính trung bình của cửa sổ ảnh
            mean_window = np.mean(window)

            # Tính toán hệ số tương quan chuẩn hóa (NCC)
            numerator = np.sum((window - mean_window) * (template - mean_template))
            denominator = np.sqrt(np.sum((window - mean_window) ** 2) * np.sum((template - mean_template) ** 2))

            # Tránh chia cho 0
            if denominator != 0:
                result[i, j] = numerator / denominator
            else:
                result[i, j] = 0
    
    return result


def sharpening_Laplacian(image):
    laplacian = cv2.Laplacian(image,cv2.CV_64F)
    sharpened_image = cv2.convertScaleAbs(image - laplacian)
    return sharpened_image

#sử dụng công thức
def median_filter_manual(data, size):
    temp = []
    indexer = size // 2
    data_final = []
    data_final = np.zeros((len(data),len(data[0])))
    for i in range(len(data)):

        for j in range(len(data[0])):

            for z in range(size):
                if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                    for c in range(size):
                        temp.append(0)
                else:
                    if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                        temp.append(0)
                    else:
                        for k in range(size):
                            temp.append(data[i + z - indexer][j + k - indexer])

            temp.sort()
            data_final[i][j] = temp[len(temp) // 2]
            temp = []
    return data_final

def mean_filter_manual(data, filter_size):
    indexer = filter_size // 2 #filter_size: Số hàng cột xung quanh tâm kernel
    data_final = np.zeros((len(data), len(data[0]))) 

    for i in range(len(data)):
        for j in range(len(data[0])):
            temp = []
            for z in range(filter_size):
                #add 0 if out of range
                if i + z - indexer < 0 or i + z - indexer > len(data) - 1:
                    for c in range(filter_size):
                        temp.append(0) 
                else:
                    #add 0 if out of range
                    if j + z - indexer < 0 or j + indexer > len(data[0]) - 1:
                        temp.append(0)
                    else:
                        for k in range(filter_size):
                            #add value to calculate mean
                            temp.append(data[i + z - indexer][j + k - indexer])

            data_final[i][j] = sum(temp) / len(temp)  #calculate mean in filter_window

    return data_final

def contra_harmonic_mean_filter(img, size, Q):
    img_height = img.shape[0]
    img_width = img.shape[1]

    img_filtered = np.zeros((img_height, img_width))
    padded_image = np.pad(img, ((size // 2, size // 2), (size // 2, size // 2)), 'constant', constant_values=0)
    for i in range(1,img_height -1):
        for j in range(img_width -1):
            # Extract the region of interest
            region = padded_image[i:i + size, j:j + size]
            numerator = np.sum(region ** (Q + 1))
            if Q == -1:
                 denominator = np.sum(1 / (region + 1e-10))
            else:
            # Calculate the numerator and denominator for the filter
                denominator = np.sum(region ** Q)
            # Apply the contra-harmonic mean formula
            ans = np.sum(numerator)
            ans1= np.sum(denominator)
            ans2 = ans/ans1
            output = round(ans2)
            img_filtered[i,j] = output
    return img_filtered


# def display_images(original, filtered):
#     plt.figure(figsize=(10, 5))

#     plt.subplot(1, 2, 1)
#     plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
#     plt.title('Original Image')
#     plt.axis('off')

#     plt.subplot(1, 2, 2)
#     plt.imshow(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))
#     plt.title('Filtered Image')
#     plt.axis('off')

#     plt.show()

# def display_images_normalized(original, filtered,template = None):
#     plt.figure(figsize=(10, 5))

#     plt.subplot(1, 3, 1)
#     plt.imshow(cv2.cvtColor(original, cv2.COLOR_BGR2RGB))
#     plt.title('Original Image')
#     plt.axis('off')

#     if template is not None:
#         plt.subplot(1, 3, 2)
#         plt.imshow(cv2.cvtColor(template, cv2.COLOR_BGR2RGB))
#         plt.title('Template Image')
#         plt.axis('off')

#     plt.subplot(1, 3, 3)
#     plt.imshow(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))
#     plt.title('Filtered Image')
#     plt.axis('off')

#     plt.show()

# #normalizedCorrelation
# original_image = Image.open("normalizedCorrelation.png").convert("L")
# arr_img = np.array(original_image)
# template = arr_img[150:300, 350:500]
# result = normalized_correlation_manual(arr_img, template)
# plt.figure(figsize=(6, 6))    
# plt.imshow(result, cmap='gray')
# plt.title("Matching Result (Manual)")
# plt.axis('off')
# plt.show()


# # img = Image.open("noiseImage.png").convert(
# #         "L")
# # arr = np.array(img)
# # removed_noise = mean_filter_manual(arr, 5) 
# # img = Image.fromarray(removed_noise)
# # img.show()


# # image_path = 'sharpening.png'
# # image = load_image(image_path)

# # filtered_image = sharpening_Laplacian(image)
# # display_images(image,filtered_image)



# #template = image[150:300, 350:500]
# #filtered_image = normalized_correletion(image, template=template)
# #display_images_normalized(image, filtered_image,template=template)


# contra_harmonic
# image = cv2.imread('salt_pepper_noisy_image.jpg', cv2.IMREAD_GRAYSCALE)
# cv2.imshow('Original Image', image)
# # filter_size = int(input("Enter filter size (single integer for square filter): "))
# # Q = float(input("Enter the value of Q: "))
# filtered_image = contra_harmonic_mean_filter(image, 3, -1)
# cv2.imshow('Filtered Image', filtered_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()