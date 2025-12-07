# NeuroGuard: Spatiotemporal Deepfake Detection System

![Python](https://img.shields.io/badge/Python-3.9-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-v2.0-red)
![License](https://img.shields.io/badge/License-MIT-green)

NeuroGuard is a forensic AI system engineered to detect deepfake videos by analyzing spatiotemporal anomalies. Unlike frame-by-frame detectors, it utilizes a hybrid Neural Network architecture to identify motion inconsistencies in facial expressions over time.

## Project Overview

The system addresses the challenge of AI-generated video manipulation by focusing on temporal dependencies. It extracts facial regions from video sequences and analyzes them using a combination of Convolutional Neural Networks (CNN) for feature extraction and Recurrent Neural Networks (RNN) for sequence classification.

## Key Features

* **Hybrid Architecture:** Implements a ResNet50 backbone combined with LSTM layers to capture both spatial features and temporal dynamics.
* **Biometric Preprocessing:** Utilizes MediaPipe for precise face tracking and cropping, ensuring the model analyzes only relevant facial data and ignores background noise.
* **Optimized Inference:** Applies Transfer Learning with frozen backbone weights, reducing computational overhead by approximately 60% while maintaining high accuracy.
* **Forensic Dashboard:** A streamlined Streamlit interface providing real-time video analysis, confidence metrics, and explainable AI (XAI) debug views.

## Technical Architecture

The pipeline consists of the following stages:

1.  **Data Ingestion:** Video input processing (MP4/AVI).
2.  **Face Extraction:** Frame-by-frame face detection and alignment.
3.  **Feature Extraction:** ResNet50 (ImageNet pre-trained) extracts a 2048-dimensional vector per frame.
4.  **Sequence Analysis:** LSTM processes sequences of 10 frames to detect temporal artifacts.
5.  **Classification:** Binary classification (Real vs. Fake) with probability scoring.

## Tech Stack

* **Language:** Python
* **Deep Learning:** PyTorch, Torchvision
* **Computer Vision:** OpenCV, MediaPipe
* **Interface:** Streamlit
* **Data Processing:** NumPy, Pandas

## Installation and Usage

1.  Clone the repository:
    ```bash
    git clone [https://github.com/yourusername/NeuroGuard.git](https://github.com/yourusername/NeuroGuard.git)
    cd NeuroGuard
    ```

2.  Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3.  Run the application:
    ```bash
    streamlit run app.py
    ```

## Model Weights

The trained model weights (`neuroguard_epoch20.pth`) are stored in the `models/` directory. Ensure this file is present before running the inference engine.

---
**Developed by Hardik Tiwari**