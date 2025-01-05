# Danh sách thuật toán
import streamlit as st
from FE_func import *

algorithms = {
    "Histogram Equalization": "Cải thiện độ tương phản của ảnh thông qua phân bổ lại histogram.",
    "Histogram Matching": "Điều chỉnh histogram của ảnh để phù hợp với ảnh tham chiếu."
}

# Widget chọn thuật toán
selected_algorithm = st.selectbox("Selected Algorithm:", list(algorithms.keys()))


if selected_algorithm == "Histogram Equalization":
    Histogram_Equalization()
if selected_algorithm == "Histogram Matching":
    histogram_matching()
 
