from FE_func import *
import streamlit as st
import requests
from PIL import Image
import zipfile
import io
import base64


st.set_page_config(page_title="Photo Editor", page_icon="📸", layout="wide")


st.markdown(
    """
    <style>
        .header {
            font-size: 50px;
            font-weight: bold;
            text-align: center;
            color: black;
            margin-bottom: 10px;
        }
        .subheader {
            font-size: 20px;
            text-align: center;
            color: #555;
        }
        .button {
            display: flex;
            justify-content: center;
            margin-top: 20px;
        }
        .popular-features {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
        }
        .feature-box {
            text-align: center;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            background-color: white;
            width: 150px;
            transition: transform 0.2s ease;
        }
        .feature-box:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.markdown('<div class="header">Online Photo Editor for Everyone</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subheader">Our online photo editor offers everything you need to enhance and edit photos effortlessly. Experience simple photo editing online for free!</div>',
    unsafe_allow_html=True,
)


# Button to Edit Photos
st.markdown(
    '<div class="button"><a href="/FFT_Filtering" style="text-decoration: none;"><button style="background-color: #0066ff; color: white; padding: 10px 20px; border: none; border-radius: 5px; font-size: 16px; cursor: pointer;">Edit Photo for Free</button></a></div>',
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)







