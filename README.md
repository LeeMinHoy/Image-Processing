# Image Processing Online 
## 🌟 Introduction
Image processing is a cornerstone of modern technology, enabling innovations across various domains, from enhancing photography to preparing data for artificial intelligence models. This project provides an advanced and user-friendly solution by combining FastAPI as the backend for robust image processing and Streamlit as the frontend for seamless interaction.

The application empowers users with tools to perform noise addition, histogram equalization, morphological operations, image compression, and more. Designed to simplify image processing tasks, it caters to developers, researchers, and enthusiasts, offering efficient and accessible solutions for diverse use cases.


## 🎯About this project
This project is designed to offer a comprehensive suite of image processing capabilities through a combination of a RESTful API and an interactive web interface.

**FastAPI Backend**: High-performance API endpoints for image processing tasks like filtering, segmentation, and transformations.

**Streamlit Frontend**: An intuitive web interface for users to upload images, tweak parameters, and visualize results instantly.

**Modular Design**: Supports various operations such as noise addition, thresholding, and compression, making it flexible for diverse use cases.


## 🎥 Simple demo

<div align="center">
  <img src="https://github.com/user-attachments/assets/f2ed8a12-cee9-420b-a764-ab26b44d06e0"/>
</div>

## 👾 Tech Stack
<details>
  <summary>Client</summary>
  <ul>
    <li><a href="https://streamlit.io/">Streamlit</a></li>
  </ul>
</details>

<details>
  <summary>Server</summary>
  <ul>
    <li><a href="https://fastapi.tiangolo.com/">FastAPI</a></li>
    <li><a href="https://www.uvicorn.org/">Uvicorn</a></li>
  </ul>
</details>

## Clone
```bash
git clone https://github.com/LeeMinHoy/Image-Processing.git
cd <repository path>
```

## ⚙️ Installation
```bash
pip install -r requirements.txt
```

## 🏃 Run Backend FastAPI server with Uvicorn:
```bash
uvicorn server:app --port 8000 --reload
```

## 🏃 Run Frontend Streamlit server: 
```bash
streamlit run FE.py
```

## Example Results

1. Negative Transformation

**Before**
<img src="https://github.com/user-attachments/assets/99081efc-2214-43f0-a6f4-0b4c6344d36a" width = "300" />
**After**
<img src="https://github.com/user-attachments/assets/ae59e4f1-97f8-4876-a002-69a1ee64d07c" width = "300" />

2. Historgram Equalization

**Before**
<img src="https://github.com/user-attachments/assets/2562593c-5542-4bb3-b0f6-b57405a5eb21" width = "300" />
**After**
<img src="https://github.com/user-attachments/assets/28deaa98-2cd7-4918-8ebf-b76cffa32b71" width = "300" />

3. Otsu Threshold Segmentation

**Before**
<img src="https://github.com/user-attachments/assets/af8e9254-e287-4573-97a4-4c58518db8dd" width = "300" />
**After**
<img src="https://github.com/user-attachments/assets/7d58c4e6-ff34-422b-9771-1509238b1ae7" width = "300" />

4. Median Filter
   
**Before**
<img src="https://github.com/user-attachments/assets/f3318dff-9a38-44a9-81cc-5dbf0b65be8a" width = "300" />
**After**
<img src="https://github.com/user-attachments/assets/1d78ebc8-a622-4526-8c60-2334367cb9d0" width = "300" />

5. Add Gaussian Noise

**Before**
<img src="https://github.com/user-attachments/assets/0c3d94bd-ecf9-4d2d-9e80-1787c02f4ec6" width = "300" />
**After**
<img src="https://github.com/user-attachments/assets/aaa4422c-b823-4f52-a4d3-448c8baf80c0" width = "300" />

6. Erosion Morphology

**Before**
<img src="https://github.com/user-attachments/assets/22967305-0131-42e1-864a-da8d428d70da" width = "300" />
**After**
<img src="https://github.com/user-attachments/assets/465823ef-cfde-45fd-bc3b-8a3b35e56fe0" width = "300" />

## 🤝 Contact
Email: minhkhoi080203@gmail.com 

Project Link: [https://github.com/LeeMinHoy/Image-Processing](https://github.com/LeeMinHoy/Image-Processing) 



