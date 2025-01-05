from FE_func import *
import streamlit as st
import requests
from PIL import Image
import zipfile
import io
import base64

# Set page config
st.set_page_config(page_title="Photo Editor", page_icon="📸", layout="wide")

# Custom CSS for enhanced visuals
st.markdown(
    """
    <style>
        body {
            background-color: #f9f9f9;
        }
        .header {
            font-size: 50px;
            font-weight: bold;
            text-align: center;
            color: #333;
            margin-bottom: 20px;
        }
        .subheader {
            font-size: 20px;
            text-align: center;
            color: #555;
            margin-bottom: 30px;
        }
        .button {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .edit-button {
            background-color: #0066ff;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
        }
        .edit-button:hover {
            background-color: #0052cc;
            box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
        }
        .popular-features {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 40px;
            flex-wrap: wrap;
        }
        .feature-box {
            text-align: center;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            background-color: white;
            width: 200px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .feature-box:hover {
            transform: scale(1.1);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
        }
        .feature-box img {
            width: 60px;
            margin-bottom: 15px;
        }
        .feature-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }
        .feature-description {
            font-size: 14px;
            color: #555;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.markdown('<div class="header">📸 Online Photo Editor for Everyone</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subheader">Enhance your photos effortlessly with our free online editor. Simple, intuitive, and packed with features!</div>',
    unsafe_allow_html=True,
)

# Button Section
st.markdown(
    """
    <div class="button">
        <a href="/FFT_Filtering" class="edit-button">🚀 Edit Photo for Free</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Popular Features Section
st.markdown(
    """
    <div class="popular-features">
        <div class="feature-box">
            <img src="https://img.icons8.com/ios-filled/100/000000/brightness.png" alt="Brightness Adjustment">
            <div class="feature-title">Brightness</div>
            <div class="feature-description">Fine-tune your photo's brightness with ease.</div>
        </div>
        <div class="feature-box">
            <img src="https://img.icons8.com/ios-filled/100/000000/crop.png" alt="Crop">
            <div class="feature-title">Crop</div>
            <div class="feature-description">Resize or crop your image to perfection.</div>
        </div>
        <div class="feature-box">
            <img src="https://img.icons8.com/ios-filled/100/000000/filter.png" alt="Filters">
            <div class="feature-title">Filters</div>
            <div class="feature-description">Apply stunning filters to make your photos stand out.</div>
        </div>
        <div class="feature-box">
            <img src="https://img.icons8.com/ios-filled/100/000000/contrast.png" alt="Contrast Adjustment">
            <div class="feature-title">Contrast</div>
            <div class="feature-description">Enhance the contrast to bring out details.</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
