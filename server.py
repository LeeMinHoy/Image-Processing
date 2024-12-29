from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
import uvicorn
from io import BytesIO
from typing import List
from fastapi.responses import StreamingResponse
import io
from PIL import Image
import os
from tempfile import NamedTemporaryFile

from Addnoise import add_gaussian_noise, add_salt_pepper_noise, add_uniform_noise
from BitPlaneSlicing import bit_plane_slicing
from HistogramProcessing import histogramEqualization, histogramMatching
from NegativeImages import negative_process
from Logarithmic import logarithmic_process
from Morphological import to_binary, erosion, dilation, opening, closing
from Segmentation import otsu_threshold_manual
from powerLaw import power_law_transform
from PieceWiseLinear import piecewiseLinear
from ThersholdImages import threshold_processing
from Filter import mean_filter, mean_filter_manual, median_filter, median_filter_manual, normalized_correletion, normalized_correlation_manual, contra_harmonic_mean_filter, sharpening_Laplacian
from FFT_filter import ideal_low_pass_filter, butterworth_low_pass_filter, gaussian_low_pass_filter, apply_filter_in_frequency_domain
from ImageCompression import rle_encode, rle_decode, calculate_rms
from jpegCompression.main import jpeg_compress, jpeg_decompress


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def read_image(file: UploadFile):
    try:
        file_bytes = BytesIO(file.file.read())
        image = cv2.imdecode(np.frombuffer(file_bytes.read(), np.uint8), cv2.IMREAD_COLOR)
        return image
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

def read_gray_image(file: UploadFile):
    try:
        file_bytes = BytesIO(file.file.read())
        image = cv2.imdecode(np.frombuffer(file_bytes.read(), np.uint8), cv2.IMREAD_GRAYSCALE)
        return image
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file")

# @app.post("/bit-plane-slicing/")
# async def process_bit_plane_slicing(image: UploadFile = File(...), bit_plane: int = 0):
#     img = read_image(image)
#     result = bit_plane_slicing(img, bit_plane)
#     _, buffer = cv2.imencode('.png', result)
#     return StreamingResponse(io.BytesIO(buffer), media_type="image/png")

import zipfile
from fastapi.responses import FileResponse

@app.post("/bit-plane-slicing/")
async def process_bit_plane_slicing(image: UploadFile = File(...)):
    # Đọc ảnh đầu vào
    img = read_image(image)

    # Tạo một file zip để lưu tất cả ảnh bitplane
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for bit_plane in range(8):  # Lặp qua các bitplanes từ 0 đến 7
            result = bit_plane_slicing(img, bit_plane)  # Gọi hàm xử lý từng bitplane
            _, buffer = cv2.imencode('.png', result)  # Mã hóa ảnh thành PNG
            # Thêm ảnh vào file zip
            zip_file.writestr(f"bit_plane_{bit_plane}.png", buffer.tobytes())

    zip_buffer.seek(0)  # Đặt con trỏ về đầu file zip

    # Trả về file zip chứa toàn bộ ảnh bitplane
    return StreamingResponse(zip_buffer, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=bit_planes.zip"})


@app.post("/histogram-equalization/")
async def process_histogram_equalization(image: UploadFile = File(...)):
    img = read_image(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = histogramEqualization(gray)
    result = np.uint8(result)
    _, buffer = cv2.imencode('.png', result)
    return StreamingResponse(io.BytesIO(buffer), media_type="image/png")

@app.post("/negative-image/")
async def process_negative_image(image: UploadFile = File(...)):
    img = read_image(image)
    negav_img = negative_process(img)
    _, buffer = cv2.imencode('.png', negav_img)
    return StreamingResponse(io.BytesIO(buffer), media_type="image/png")

@app.post("/logarithmic/")
async def process_logarithmic(image: UploadFile = File(...)):
    img = read_image(image)
    log_img = logarithmic_process(img)
    _, buffer = cv2.imencode('.png', log_img)
    return StreamingResponse(io.BytesIO(buffer), media_type="image/png")

@app.post("/morphological/erosion/")
async def process_erosion(image: UploadFile = File(...), kernel_size: int = 3):
    img = read_image(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary_image = to_binary(gray)
    inverted_binary_image = cv2.bitwise_not(binary_image)
    result = erosion(inverted_binary_image, kernel_size)
    _, buffer = cv2.imencode('.png', result)
    return StreamingResponse(io.BytesIO(buffer), media_type="image/png")

@app.post("/morphological/dilation/")
async def process_dilation(image: UploadFile = File(...), kernel_size: int = 3):
    img = read_image(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary_image = to_binary(gray)
    inverted_binary_image = cv2.bitwise_not(binary_image)
    result = dilation(inverted_binary_image, kernel_size)
    _, buffer = cv2.imencode('.png', result)
    return StreamingResponse(io.BytesIO(buffer), media_type="image/png")

@app.post("/morphological/opening/")
async def process_opening(image: UploadFile = File(...), kernel_size: int = 3):
    img = read_image(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary_image = to_binary(gray)
    inverted_binary_image = cv2.bitwise_not(binary_image)
    result = opening(inverted_binary_image, kernel_size)
    _, buffer = cv2.imencode('.png', result)
    return StreamingResponse(io.BytesIO(buffer), media_type="image/png")

@app.post("/morphological/closing/")
async def process_closing(image: UploadFile = File(...), kernel_size: int = 3):
    img = read_image(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary_image = to_binary(gray)
    inverted_binary_image = cv2.bitwise_not(binary_image)
    result = closing(inverted_binary_image, kernel_size)
    _, buffer = cv2.imencode('.png', result)
    return StreamingResponse(io.BytesIO(buffer), media_type="image/png")


@app.post("/otsu-threshold/")
async def otsu_threshold(image: UploadFile = File(...)):
    img = read_image(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    otsu_threshold_value = otsu_threshold_manual(gray)
    _, thresholded_image = cv2.threshold(gray, otsu_threshold_value, 255, cv2.THRESH_BINARY)
    
    _, buffer = cv2.imencode('.png', thresholded_image)
    print(otsu_threshold_value)
    return StreamingResponse(io.BytesIO(buffer), media_type="image/png")

@app.post("/powerlaw/")
async def process_power_law(image: UploadFile = File(...), gamma: float = 0.4):
    img = read_image(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = power_law_transform(gray, gamma)
    _, buffer = cv2.imencode('.png', result)
    return StreamingResponse(io.BytesIO(buffer), media_type="image/png")

@app.post("/piecewise-linear/")
async def process_piecewise_linear(image: UploadFile = File(...), r1: int = 90, s1: int = 40, r2: int = 180, s2: int = 220):
    img = read_image(image)
    transformed_img = piecewiseLinear(img, r1, s1, r2, s2)
    _, buffer = cv2.imencode('.png', transformed_img)
    return StreamingResponse(BytesIO(buffer), media_type="image/png")

@app.post("/threshold-processing/")
async def process_threshold(image: UploadFile = File(...), threshold: int = 50):
    img = read_image(image)
    thresholded_img = threshold_processing(img, threshold)
    _, buffer = cv2.imencode('.png', thresholded_img)
    
    return StreamingResponse(BytesIO(buffer), media_type="image/png")

@app.post("/mean-filter-manual/")
async def process_mean_filter_manual(image: UploadFile = File(...), size: int = 3):
    img = read_image(image)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    filtered_img = mean_filter_manual(gray_img, size)
    filtered_img = np.uint8(filtered_img)
    _, buffer = cv2.imencode('.png', filtered_img)
    
    return StreamingResponse(BytesIO(buffer), media_type="image/png")

@app.post("/mean-filter/")
async def process_mean_filter(image: UploadFile = File(...), size: int = 3):
    img = read_image(image)
    mean_filtered_img = mean_filter(img, size)
    _, buffer = cv2.imencode('.png', mean_filtered_img)
    return StreamingResponse(BytesIO(buffer), media_type="image/png")

@app.post("/median-filter-manual/")
async def process_median_filter_manual(image: UploadFile = File(...), size: int = 3):
    img = read_image(image)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    filtered_img = median_filter_manual(gray_img, size)
    filtered_img = np.uint8(filtered_img)
    _, buffer = cv2.imencode('.png', filtered_img)
    
    return StreamingResponse(BytesIO(buffer), media_type="image/png")

@app.post("/median-filter/")
async def process_median_filter(image: UploadFile = File(...), size: int = 3):
    img = read_image(image)
    median_filtered_img = median_filter(img, size)
    _, buffer = cv2.imencode('.png', median_filtered_img)
    return StreamingResponse(BytesIO(buffer), media_type="image/png")

@app.post("/normalized-correlation/")
async def process_normalized_correlation(image: UploadFile = File(...), template: UploadFile = File(...)):
    img = read_image(image)
    template_img = read_image(template)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)
    result = normalized_correletion(gray_img, gray_template)
    _, buffer = cv2.imencode('.png', result)
    
    return StreamingResponse(BytesIO(buffer), media_type="image/png")

@app.post("/normalized-correlation-manual/")
async def process_normalized_correlation_manual(image: UploadFile = File(...), template: UploadFile = File(...)):
    img = read_image(image)
    template_img = read_image(template)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_template = cv2.cvtColor(template_img, cv2.COLOR_BGR2GRAY)
    result = normalized_correlation_manual(gray_img, gray_template)
    _, buffer = cv2.imencode('.png', result)
    
    return StreamingResponse(BytesIO(buffer), media_type="image/png")

@app.post("/contra-harmonic-filter/")
async def process_contra_harmonic_filter(image: UploadFile = File(...), size: int = 3, Q: float = -1):
    img = read_image(image)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    filtered_img = contra_harmonic_mean_filter(gray_img, size, Q)
    _, buffer = cv2.imencode('.png', filtered_img)
    
    return StreamingResponse(BytesIO(buffer), media_type="image/png")

@app.post("/sharpening-laplacian/")
async def process_sharpening_laplacian(image: UploadFile = File(...)):
    img = read_image(image)
    sharpened_img = sharpening_Laplacian(img)
    _, buffer = cv2.imencode('.png', sharpened_img)
    
    return StreamingResponse(BytesIO(buffer), media_type="image/png")

@app.post("/apply-frequency-filter/")
async def apply_frequency_filter(image: UploadFile = File(...), filter_type: str = "gaussian", cutoff: float = 50, order: int = 2):
    img = read_gray_image(image)
    if filter_type == "ideal":
        filter_mask = ideal_low_pass_filter(img.shape, cutoff)
    elif filter_type == "butterworth":
        filter_mask = butterworth_low_pass_filter(img.shape, cutoff, order)
    elif filter_type == "gaussian":
        filter_mask = gaussian_low_pass_filter(img.shape, cutoff)
    else:
        raise HTTPException(status_code=400, detail="Invalid filter type")
    filtered_img = apply_filter_in_frequency_domain(img, filter_mask)
    _, buffer = cv2.imencode('.png', filtered_img)
    
    return StreamingResponse(BytesIO(buffer), media_type="image/png")

    

@app.post("/add-gaussian-noise/")
async def process_gaussian_noise(image: UploadFile = File(...), mean: float = 0, sigma: float = 25):
    img = read_image(image)
    
    # Thêm nhiễu Gaussian vào ảnh
    noisy_img = add_gaussian_noise(img, mean, sigma)
    
    # Mã hóa ảnh kết quả sang định dạng PNG
    _, buffer = cv2.imencode('.png', noisy_img)
    
    return StreamingResponse(BytesIO(buffer), media_type="image/png")

@app.post("/add-uniform-noise/")
async def process_uniform_noise(image: UploadFile = File(...), low: float = -50, high: float = 50):
    img = read_image(image)
    
    # Thêm nhiễu Uniform vào ảnh
    noisy_img = add_uniform_noise(img, low, high)
    
    # Mã hóa ảnh kết quả sang định dạng PNG
    _, buffer = cv2.imencode('.png', noisy_img)
    
    return StreamingResponse(BytesIO(buffer), media_type="image/png")

@app.post("/add-salt-pepper-noise/")
async def process_salt_pepper_noise(image: UploadFile = File(...), salt_prob: float = 0.01, pepper_prob: float = 0.01):
    img = read_image(image)
    
    # Thêm nhiễu Salt-and-Pepper vào ảnh
    noisy_img = add_salt_pepper_noise(img, salt_prob, pepper_prob)
    
    # Mã hóa ảnh kết quả sang định dạng PNG
    _, buffer = cv2.imencode('.png', noisy_img)
    
    return StreamingResponse(BytesIO(buffer), media_type="image/png")

@app.post("/histogram-matching/")
async def process_histogram_matching(source_image: UploadFile = File(...), reference_image: UploadFile = File(...)):
    source_img = read_gray_image(source_image)
    reference_img = read_gray_image(reference_image)

    # Thực hiện Histogram Matching
    matched_img = histogramMatching(source_img, reference_img)

    # Mã hóa ảnh kết quả sang định dạng PNG
    _, buffer = cv2.imencode('.png', matched_img)
    
    return StreamingResponse(BytesIO(buffer), media_type="image/png")

@app.post("/compression_rle/")
async def compress_decompress_image(image: UploadFile = File(...)):
    img = read_image(image)
    pixels = list(img.flatten())
    encoded = rle_encode(pixels)
    decoded_pixels = rle_decode(encoded)
    rms = calculate_rms(pixels, decoded_pixels)
    print(rms)
    decoded_image = Image.new('L', img.size)  # Chú ý đổi chiều size từ (height, width) -> (width, height)
    decoded_image.putdata(decoded_pixels)
    _, buffer = cv2.imencode('.png', np.array(decoded_image))
    
    return StreamingResponse(BytesIO(buffer), media_type="image/png")

@app.post("/jpeg-process/")
async def jpeg_process(image: UploadFile = File(...)):
    try:
        # Lưu tệp ảnh đầu vào tạm thời
        input_temp = NamedTemporaryFile(delete=False, suffix=".jpg")
        input_temp.write(await image.read())
        input_temp.close()

        # Tạo tệp nén tạm thời
        compressed_temp = NamedTemporaryFile(delete=False, suffix=".bin")
        compressed_temp.close()

        # Gọi hàm nén JPEG
        jpeg_compress(input_temp.name, compressed_temp.name)

        # Xóa tệp ảnh gốc tạm thời
        os.unlink(input_temp.name)

        # Tạo tệp giải nén tạm thời
        decompressed_temp = NamedTemporaryFile(delete=False, suffix=".jpg")
        decompressed_temp.close()

        # Gọi hàm giải nén JPEG
        jpeg_decompress(compressed_temp.name, decompressed_temp.name)

        # Xóa tệp nén tạm thời
        os.unlink(compressed_temp.name)

        # Trả về tệp ảnh JPEG đã giải nén
        return FileResponse(decompressed_temp.name, media_type="image/jpeg", filename="processed_image.jpg")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during JPEG processing: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
