import numpy as np
from PIL import Image
import scipy.fftpack
from collections import Counter
import pickle

# Utility: Save intermediate debug images
def save_debug_channels(Y, Cb, Cr, prefix="debug"):
    Image.fromarray(Y.astype(np.uint8)).save(f"{prefix}_Y.jpg")
    Image.fromarray(Cb.astype(np.uint8)).save(f"{prefix}_Cb.jpg")
    Image.fromarray(Cr.astype(np.uint8)).save(f"{prefix}_Cr.jpg")

# 1. Read and Pad Image
def read_image(path):
    img = Image.open(path)
    img = img.convert('RGB')  # Ensure RGB format
    img_array = np.array(img, dtype=np.float32)
    h, w, _ = img_array.shape

    # Pad to ensure dimensions divisible by 16 (for chroma subsampling and 8x8 blocks)
    pad_h = (16 - (h % 16)) % 16
    pad_w = (16 - (w % 16)) % 16
    if pad_h != 0 or pad_w != 0:
        img_array = np.pad(
            img_array,
            ((0, pad_h), (0, pad_w), (0, 0)),
            mode='edge'  # Use edge padding
        )
        print(f"Padded image: +{pad_h} height, +{pad_w} width")
    return img_array

# 2. RGB to YCbCr Conversion
def rgb_to_ycbcr(img):
    xform = np.array([[0.299, 0.587, 0.114],
                      [-0.168736, -0.331264, 0.5],
                      [0.5, -0.418688, -0.081312]])
    ycbcr = img.dot(xform.T)
    ycbcr[:, :, [1, 2]] += 128  # Offset Cb and Cr
    return ycbcr

# 3. Chroma Subsampling (4:2:0)
def chroma_subsampling(ycbcr):
    Y = ycbcr[:, :, 0]
    Cb = ycbcr[:, :, 1]
    Cr = ycbcr[:, :, 2]
    Cb_sub = Cb[::2, ::2]
    Cr_sub = Cr[::2, ::2]
    return Y, Cb_sub, Cr_sub

# 4. Split into 8x8 Blocks
def split_into_blocks(channel):
    h, w = channel.shape
    h_pad = (8 - h % 8) % 8
    w_pad = (8 - w % 8) % 8
    channel_padded = np.pad(channel, ((0, h_pad), (0, w_pad)), mode='constant', constant_values=0)
    blocks = [channel_padded[i:i+8, j:j+8] for i in range(0, channel_padded.shape[0], 8) for j in range(0, channel_padded.shape[1], 8)]
    return blocks, channel_padded.shape

# 5. DCT and Quantization
def dct_2d(block):
    block_shifted = block - 128
    return scipy.fftpack.dct(scipy.fftpack.dct(block_shifted.T, norm='ortho').T, norm='ortho')

def quantize(block, Q):
    return np.round(block / Q)

# 6. Zig-Zag Scanning
def zigzag(block):
    index_order = sorted(((x, y) for x in range(8) for y in range(8)),
                         key=lambda s: (s[0]+s[1], -s[0] if (s[0]+s[1])%2 else s[0]))
    return np.array([block[i, j] for i, j in index_order])

# 7. Huffman Encoding (Simplified)
def build_huffman_table(data):
    frequency = Counter(data)
    sorted_items = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
    return {k: format(i, '08b') for i, (k, _) in enumerate(sorted_items)}

def huffman_encode(data, huffman_table):
    return ''.join(huffman_table[item] for item in data)

# 8. Process Channels
def process_channel(channel, Q):
    blocks, shape = split_into_blocks(channel)
    dct_blocks = [dct_2d(block) for block in blocks]
    quantized_blocks = [quantize(block, Q) for block in dct_blocks]
    zigzag_blocks = [zigzag(block) for block in quantized_blocks]
    flat_data = np.concatenate(zigzag_blocks).astype(int)
    huffman_table = build_huffman_table(flat_data)
    encoded_data = huffman_encode(flat_data, huffman_table)
    return encoded_data, huffman_table, shape

# 9. JPEG Compress
def jpeg_compress(image_path, output_path):
    img = read_image(image_path)
    ycbcr = rgb_to_ycbcr(img)
    Y, Cb, Cr = chroma_subsampling(ycbcr)

    Q_Y = np.array([[16,11,10,16,24,40,51,61],
                    [12,12,14,19,26,58,60,55],
                    [14,13,16,24,40,57,69,56],
                    [14,17,22,29,51,87,80,62],
                    [18,22,37,56,68,109,103,77],
                    [24,35,55,64,81,104,113,92],
                    [49,64,78,87,103,121,120,101],
                    [72,92,95,98,112,100,103,99]])

    Q_C = np.array([[17,18,24,47,99,99,99,99],
                    [18,21,26,66,99,99,99,99],
                    [24,26,56,99,99,99,99,99],
                    [47,66,99,99,99,99,99,99],
                    [99,99,99,99,99,99,99,99],
                    [99,99,99,99,99,99,99,99],
                    [99,99,99,99,99,99,99,99],
                    [99,99,99,99,99,99,99,99]])

    Y_encoded, Y_huffman_table, Y_shape = process_channel(Y, Q_Y)
    Cb_encoded, Cb_huffman_table, Cb_shape = process_channel(Cb, Q_C)
    Cr_encoded, Cr_huffman_table, Cr_shape = process_channel(Cr, Q_C)

    compressed_data = {
        'Y': Y_encoded,
        'Cb': Cb_encoded,
        'Cr': Cr_encoded,
        'Y_huffman_table': Y_huffman_table,
        'Cb_huffman_table': Cb_huffman_table,
        'Cr_huffman_table': Cr_huffman_table,
        'Y_shape': Y_shape,
        'Cb_shape': Cb_shape,
        'Cr_shape': Cr_shape,
    }

    with open(output_path, 'wb') as f:
        pickle.dump(compressed_data, f)

    print(f"Compressed data saved to {output_path}")

# 10. JPEG Decompress
def jpeg_decompress(compressed_path, output_path):
    with open(compressed_path, 'rb') as f:
        compressed_data = pickle.load(f)

    Y_shape = compressed_data['Y_shape']
    Cb_shape = compressed_data['Cb_shape']
    Cr_shape = compressed_data['Cr_shape']
    Q_Y = np.array([[16,11,10,16,24,40,51,61],
                    [12,12,14,19,26,58,60,55],
                    [14,13,16,24,40,57,69,56],
                    [14,17,22,29,51,87,80,62],
                    [18,22,37,56,68,109,103,77],
                    [24,35,55,64,81,104,113,92],
                    [49,64,78,87,103,121,120,101],
                    [72,92,95,98,112,100,103,99]])

    Q_C = np.array([[17,18,24,47,99,99,99,99],
                    [18,21,26,66,99,99,99,99],
                    [24,26,56,99,99,99,99,99],
                    [47,66,99,99,99,99,99,99],
                    [99,99,99,99,99,99,99,99],
                    [99,99,99,99,99,99,99,99],
                    [99,99,99,99,99,99,99,99],
                    [99,99,99,99,99,99,99,99]])

    def huffman_decode(encoded_str, huffman_table):
        reverse_table = {v: k for k, v in huffman_table.items()}
        decoded_data = []
        code = ''
        for bit in encoded_str:
            code += bit
            if code in reverse_table:
                decoded_data.append(reverse_table[code])
                code = ''
        return decoded_data

    def inverse_zigzag(data):
        zigzag_order = sorted(((x, y) for x in range(8) for y in range(8)),
                              key=lambda s: (s[0]+s[1], -s[0] if (s[0]+s[1])%2 else s[0]))
        block = np.zeros((8, 8))
        for idx, (i, j) in enumerate(zigzag_order):
            block[i, j] = data[idx]
        return block

    def idct_2d(block):
        return scipy.fftpack.idct(scipy.fftpack.idct(block.T, norm='ortho').T, norm='ortho') + 128

    def reconstruct_channel(decoded_data, huffman_table, Q, shape):
        blocks = [decoded_data[i:i+64] for i in range(0, len(decoded_data), 64)]
        quantized_blocks = [inverse_zigzag(block) * Q for block in blocks]
        spatial_blocks = [idct_2d(block) for block in quantized_blocks]

        h_padded, w_padded = shape
        channel_padded = np.zeros((h_padded, w_padded))
        idx = 0
        for i in range(0, h_padded, 8):
            for j in range(0, w_padded, 8):
                channel_padded[i:i+8, j:j+8] = spatial_blocks[idx]
                idx += 1
        return channel_padded

    Y_decoded = huffman_decode(compressed_data['Y'], compressed_data['Y_huffman_table'])
    Cb_decoded = huffman_decode(compressed_data['Cb'], compressed_data['Cb_huffman_table'])
    Cr_decoded = huffman_decode(compressed_data['Cr'], compressed_data['Cr_huffman_table'])

    Y_reconstructed = reconstruct_channel(Y_decoded, compressed_data['Y_huffman_table'], Q_Y, Y_shape)
    Cb_reconstructed = reconstruct_channel(Cb_decoded, compressed_data['Cb_huffman_table'], Q_C, Cb_shape)
    Cr_reconstructed = reconstruct_channel(Cr_decoded, compressed_data['Cr_huffman_table'], Q_C, Cr_shape)

    def chroma_upsampling(C_sub, shape):
        h, w = shape
        C = np.repeat(np.repeat(C_sub, 2, axis=0), 2, axis=1)
        return C[:h, :w]

    Cb_up = chroma_upsampling(Cb_reconstructed, Y_shape)
    Cr_up = chroma_upsampling(Cr_reconstructed, Y_shape)

    save_debug_channels(Y_reconstructed, Cb_up, Cr_up, "reconstructed_debug")

    def ycbcr_to_rgb(Y, Cb, Cr):
        Cb -= 128
        Cr -= 128
        R = Y + 1.402 * Cr
        G = Y - 0.344136 * Cb - 0.714136 * Cr
        B = Y + 1.772 * Cb
        rgb = np.stack((R, G, B), axis=2)
        return np.clip(rgb, 0, 255).astype(np.uint8)

    rgb = ycbcr_to_rgb(Y_reconstructed, Cb_up, Cr_up)
    Image.fromarray(rgb).save(output_path)
    print(f"Decompressed image saved to {output_path}")

# Example Usage
# jpeg_compress('./jpegCompression/realraw.dng', 'compressed.bin')
# jpeg_decompress('compressed.bin', './jpegCompression/reconstructed.jpg')
