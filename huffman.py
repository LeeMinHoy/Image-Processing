import heapq
from collections import defaultdict
from PIL import Image
import pickle

# Node của cây Huffman
class HuffmanNode:
    def __init__(self, pixel, freq):
        self.pixel = pixel
        self.freq = freq
        self.left = None
        self.right = None

    # Định nghĩa để heapq có thể so sánh các node
    def __lt__(self, other):
        return self.freq < other.freq

# Xây dựng cây Huffman từ tần số xuất hiện của các pixel
def build_huffman_tree(frequency):
    heap = []
    for pixel, freq in frequency.items():
        heapq.heappush(heap, HuffmanNode(pixel, freq))
    
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
    
    return heap[0] if heap else None

# Tạo bảng mã từ cây Huffman
def build_codes(node, current_code, codes):
    if node is None:
        return
    if node.pixel is not None:
        codes[node.pixel] = current_code
        return
    build_codes(node.left, current_code + "0", codes)
    build_codes(node.right, current_code + "1", codes)

# Mã hóa dữ liệu ảnh
def huffman_encode(image_path, encoded_path, codebook_path):
    image = Image.open(image_path).convert('L')  # Chuyển ảnh sang grayscale
    pixels = list(image.getdata())
    frequency = defaultdict(int)
    for pixel in pixels:
        frequency[pixel] += 1
    
    root = build_huffman_tree(frequency)
    codes = {}
    build_codes(root, "", codes)
    
    # Mã hóa dữ liệu
    encoded_data = ''.join([codes[pixel] for pixel in pixels])
    
    # Lưu bảng mã và dữ liệu mã hóa
    with open(codebook_path, 'wb') as f:
        pickle.dump(codes, f)
    
    with open(encoded_path, 'w') as f:
        f.write(encoded_data)
    
    print("Mã hóa hoàn tất!")

# Giải mã dữ liệu ảnh
def huffman_decode(encoded_path, codebook_path, output_image_path, image_size):
    # Tải bảng mã
    with open(codebook_path, 'rb') as f:
        codes = pickle.load(f)
    
    # Đảo bảng mã để dễ dàng tìm kiếm
    inverse_codes = {v: k for k, v in codes.items()}
    
    # Đọc dữ liệu mã hóa
    with open(encoded_path, 'r') as f:
        encoded_data = f.read()
    
    decoded_pixels = []
    current_code = ""
    for bit in encoded_data:
        current_code += bit
        if current_code in inverse_codes:
            decoded_pixels.append(inverse_codes[current_code])
            current_code = ""
            if len(decoded_pixels) == image_size[0] * image_size[1]:
                break
    
    # Tạo ảnh từ dữ liệu giải mã
    decoded_image = Image.new('L', image_size)
    decoded_image.putdata(decoded_pixels)
    decoded_image.save(output_image_path)
    
    print("Giải mã hoàn tất! Ảnh đã được lưu tại:", output_image_path)

# Ví dụ sử dụng
if __name__ == "__main__":
    # Đường dẫn tới ảnh gốc
    original_image = 'bitplaneslicing.png'  # Thay thế bằng đường dẫn tới ảnh của bạn
    
    # Đường dẫn lưu dữ liệu mã hóa và bảng mã
    encoded_file = 'encoded.bin'
    codebook_file = 'codebook.pkl'
    
    # Đường dẫn lưu ảnh giải mã
    decoded_image = 'decoded_image_huffman.png'
    
    # Mã hóa ảnh
    huffman_encode(original_image, encoded_file, codebook_file)
    
    # Giải mã ảnh
    # Cần biết kích thước ảnh gốc để giải mã chính xác
    image = Image.open(original_image)
    image_size = image.size  # (width, height)
    huffman_decode(encoded_file, codebook_file, decoded_image, image_size)
