# Danh sách thuật toán
import streamlit as st
from FE_func import *

algorithms = {
    "Mean Filter": "Áp dụng bộ lọc trung bình để làm mịn ảnh bằng cách giảm nhiễu.",
    "Median Filter": "Sử dụng bộ lọc trung vị để giảm nhiễu và bảo toàn cạnh trong ảnh.",
    "Normalized Correlation": "Tính toán độ tương quan bình thường hóa giữa các vùng ảnh.",
    "Sharpening Laplacian": "Làm sắc nét ảnh bằng cách sử dụng bộ lọc Laplacian.",
    "Contra Harmonic Mean Filter": "Áp dụng bộ lọc trung bình nghịch đảo để giảm nhiễu cụ thể."
}


# Widget chọn thuật toán
selected_algorithm = st.selectbox("Chọn thuật toán:", list(algorithms.keys()))

if selected_algorithm == "Mean Filter":
    mean_filter()
if selected_algorithm == "Median Filter":
    median_filter()
if selected_algorithm == "Normalized Correlation":
    normalized_correlation()
if selected_algorithm == "Sharpening Laplacian":
    sharpening_laplacian()
if selected_algorithm == "Contra Harmonic Mean Filter":
    hamonic()

