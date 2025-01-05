
# Danh sách thuật toán
import streamlit as st
from FE_func import *

algorithms = {
    "Add Gaussian Noise": "Thêm nhiễu Gaussian vào ảnh với tham số mean và sigma.",
    "Add Uniform Noise": "Thêm nhiễu Uniform vào ảnh với các giá trị trong khoảng [low, high].",
    "Add Salt and Pepper Noise": "Thêm nhiễu Salt-and-Pepper vào ảnh để mô phỏng nhiễu ngẫu nhiên."
}




# Widget chọn thuật toán
selected_algorithm = st.selectbox("Chọn thuật toán:", list(algorithms.keys()))

if selected_algorithm == "Add Gaussian Noise":
    add_gaussian_noise()

if selected_algorithm == "Add Uniform Noise":
    add_uniform_noise()

if selected_algorithm == "Add Salt and Pepper Noise":
    add_salt_pepper_noise()


