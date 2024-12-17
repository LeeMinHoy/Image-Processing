from PIL import Image
import math
def rle_encode(data):
    encoding = []
    prev_char = data[0] #Gán giá trị đầu tiên xuất hiện
    count = 1

    for char in data[1:]: #So sánh với giá trị hàng thứ 2
        if char == prev_char:
            count += 1
        else:
            encoding.append((prev_char, count))
            prev_char = char
            count = 1
    encoding.append((prev_char, count))
    return encoding

def rle_decode(encoded):
    decoded = []
    for char, count in encoded:
        decoded.extend([char] * count)
    return decoded

def calculate_rms(original, decoded):
    if len(original) != len(decoded):
        raise ValueError("Hai ảnh phải có cùng số lượng pixel để tính RMS.")
    
    mse = 0
    for o, d in zip(original, decoded):
        mse += (o - d) ** 2
    mse /= len(original)
    rms = math.sqrt(mse)
    return rms

# image = Image.open('bitplaneslicing.png').convert('L')  # 'L' cho grayscale
# pixels = list(image.getdata())

# encoded = rle_encode(pixels)
# print("Encoded RLE:", encoded)

# decoded_pixels = rle_decode(encoded)

# rms = calculate_rms(pixels, decoded_pixels)
# print(f"RMS giữa ảnh gốc và ảnh đã giải mã: {rms}")

# # Tạo ảnh từ dữ liệu đã giải mã
# decoded_image = Image.new('L', image.size) #decode height width
# decoded_image.putdata(decoded_pixels)
# decoded_image.save('decoded_image.png')
