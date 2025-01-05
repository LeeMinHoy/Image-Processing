# Danh sách thuật toán
import streamlit as st
from FE_func import *

algorithms = {
    "Negative Images": "Chuyển đổi ảnh thành dạng âm bản.",
    "Threshold Image": "Phân ngưỡng để chuyển đổi ảnh thành ảnh nhị phân dựa trên giá trị ngưỡng.",
    "Logarithmic": "Áp dụng phép biến đổi log để nén dải động của ảnh.",
    "PowerLaw": "Thay đổi độ sáng và độ tương phản của ảnh bằng phép biến đổi lũy thừa.",
    "Piecewise": "Áp dụng phép biến đổi tuyến tính theo từng đoạn để cải thiện độ tương phản.",
    "Bit plane Slicing": "Phân tích và hiển thị từng mặt phẳng bit của ảnh."
}

# Widget chọn thuật toán
selected_algorithm = st.selectbox("Chọn thuật toán:", list(algorithms.keys()))

if selected_algorithm == "Negative Images":
    negative_image()

if selected_algorithm == "Threshold Image":
    threshold_processing()

if selected_algorithm == "Logarithmic":
    logarithmic()

if selected_algorithm == "PowerLaw":
   powerlaw()

if selected_algorithm == "Piecewise":
    piecewise_linear()

if selected_algorithm == "Bit plane Slicing":
    Bit_Plane_Slicing()
