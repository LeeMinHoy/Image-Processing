# Danh sách thuật toán
import streamlit as st
from FE_func import *

algorithms = {
    "Morphological Erosion": "Áp dụng phép co ảnh (erosion) để loại bỏ các chi tiết nhỏ hoặc làm mỏng đường biên.",
    "Morphological Dilation": "Áp dụng phép giãn ảnh (dilation) để mở rộng các chi tiết hoặc làm dày đường biên.",
    "Morphological Opening": "Áp dụng phép mở ảnh (opening) để loại bỏ nhiễu nhỏ và giữ lại cấu trúc chính.",
    "Morphological Closing": "Áp dụng phép đóng ảnh (closing) để lấp đầy lỗ hổng nhỏ và làm mịn đường biên."
}



# Widget chọn thuật toán
selected_algorithm = st.selectbox("Chọn thuật toán:", list(algorithms.keys()))

if selected_algorithm == "Morphological Erosion":
    morphological_erosion()

if selected_algorithm == "Morphological Dilation":
    morphological_dilation()

if selected_algorithm == "Morphological Opening":
    morphological_opening()

if selected_algorithm == "Morphological Closing":
    morphological_closing()

