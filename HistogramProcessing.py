import numpy as np
import cv2
def float2int(img):
    img = np.round(img, 0)
    img = np.minimum(img, 255)
    img = np.maximum(img, 0)
    img = img.astype('uint8')
    
    return img

def histogramEqualization(img):
    img_height = img.shape[0]
    img_width = img.shape[1]
    histogram = np.zeros([256], np.int32)
    for i in range (0, img_height):
        for j in range (0, img_width):
            histogram[img[i,j]] += 1

    pdf = histogram/histogram.sum()
    cdf = np.zeros([256],float)

    cdf[0] = pdf[0]
    for i in range (1,256):
        cdf[i] = cdf[i-1]+ pdf[i]

    cdf_eq = np.round(cdf * 255,0)
    imgEqualized = np.zeros((img_height, img_width))
    
    # map input image to s.
    for i in range(0, img_height):
        for j in range(0, img_width):
            r = img[i, j]
            s = cdf_eq[r]
            imgEqualized[i, j] = s 
    
    return imgEqualized

def compute_histogram(image):
    hist = np.zeros(256)
    for pixel in image.ravel():
        hist[pixel] += 1
    return hist / np.sum(hist)

def compute_cdf(hist):
    return np.cumsum(hist)

def histogram_matching(source, template):
    source_hist = compute_histogram(source)
    template_hist = compute_histogram(template)

    source_cdf = compute_cdf(source_hist)
    template_cdf = compute_cdf(template_hist)

    # Create the mapping from source to template
    mapping = np.zeros(256, dtype=np.uint8)
    template_value = 0

    for i in range(256):
        while template_value < 255 and template_cdf[template_value] < source_cdf[i]:
            template_value += 1
        mapping[i] = template_value

    matched_image = np.zeros_like(source)
    for i in range(source.shape[0]):
        for j in range(source.shape[1]):
            matched_image[i, j] = mapping[source[i, j]]

    return matched_image

def histogramMatching(source_img, reference_img):
    source_height, source_width = source_img.shape
    reference_hist = np.zeros([256], np.int32)

    for i in range(0, reference_img.shape[0]):
        for j in range(0, reference_img.shape[1]):
            reference_hist[reference_img[i, j]] += 1

    reference_pdf = reference_hist / reference_hist.sum()
    reference_cdf = np.zeros([256], float)

    reference_cdf[0] = reference_pdf[0]
    for i in range(1, 256):
        reference_cdf[i] = reference_cdf[i - 1] + reference_pdf[i]

    source_cdf_eq = np.zeros([256], float)
    source_hist = np.zeros([256], np.int32)

    for i in range(0, source_height):
        for j in range(0, source_width):
            source_hist[source_img[i, j]] += 1

    source_pdf = source_hist / source_hist.sum()
    source_cdf_eq[0] = source_pdf[0]
    
    for i in range(1, 256):
        source_cdf_eq[i] = source_cdf_eq[i - 1] + source_pdf[i]

    mapping = np.zeros(256, dtype='uint8')
    for i in range(256):
        min_diff = np.abs(reference_cdf - source_cdf_eq[i]).min()
        mapping[i] = np.where(np.abs(reference_cdf - source_cdf_eq[i]) == min_diff)[0][0]

    matched_img = np.zeros_like(source_img)
    for i in range(0, source_height):
        for j in range(0, source_width):
            matched_img[i, j] = mapping[source_img[i, j]]

    return matched_img


# img_low = cv2.imread('image.png', cv2.IMREAD_GRAYSCALE)

# img_eq_low = histogramEqualization(img_low)
# img_eq_low = float2int(img_eq_low)

# cv2.imshow('img_eq_low', img_eq_low)
# cv2.waitKey()

# source = cv2.imread('source.png', cv2.IMREAD_GRAYSCALE)
# template = cv2.imread('template.png', cv2.IMREAD_GRAYSCALE)
# matched_image = histogramMatching(source, template)
# matched_image = float2int(matched_image)
#     # Display the images
# cv2.imshow('Source Image', source)
# cv2.imshow('Template Image', template)
# cv2.imshow('Matched Image', matched_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
