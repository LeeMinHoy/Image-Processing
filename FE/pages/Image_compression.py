
# Danh sách thuật toán
import streamlit as st
from FE_func import *

algorithms = {
    "JPEG Compress": "Thực hiện nén và giải nén ảnh JPEG để giảm kích thước tệp.",
    # "Compression RLE": "Áp dụng thuật toán nén RLE (Run-Length Encoding) để giảm kích thước dữ liệu ảnh."
}





# Widget chọn thuật toán
selected_algorithm = st.selectbox("Chọn thuật toán:", list(algorithms.keys()))

if selected_algorithm == "JPEG Compress":
    jpeg_process()



