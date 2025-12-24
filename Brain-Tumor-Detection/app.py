import streamlit as st
import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import os

# Import your custom architecture
from model import BrainTumorModel

# --- 1. DYNAMIC PATH SETUP ---
# This ensures the app finds the weights regardless of where you run it from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Logic to find the .pth file correctly
if os.path.basename(BASE_DIR) == "models":
    MODEL_PATH = os.path.join(BASE_DIR, "brain_tumor_attention_v1.pth")
else:
    MODEL_PATH = os.path.join(BASE_DIR, "models", "brain_tumor_attention_v1.pth")

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# --- 2. LOAD MODEL ---
@st.cache_resource
def load_trained_model():
    # Initialize the EfficientNet + Attention model
    model = BrainTumorModel(num_classes=4)
    
    if not os.path.exists(MODEL_PATH):
        st.error(f"❌ WEIGHTS NOT FOUND! Looking at: {MODEL_PATH}")
        st.stop()
    
    # Load the 99.49% accuracy weights
    checkpoint = torch.load(MODEL_PATH, map_location=DEVICE)
    model.load_state_dict(checkpoint)
    model.to(DEVICE)
    model.eval()
    return model

# --- 3. PREPROCESSING ---
def preprocess_image(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    return transform(image).unsqueeze(0).to(DEVICE)

# --- 4. UI INTERFACE ---
st.set_page_config(page_title="Brain Tumor AI", page_icon="🧠")

st.title("🧠 Brain Tumor Diagnostic Engine")
st.write("Using **EfficientNet-B0 + Attention Mechanism** for high-precision MRI analysis.")

# Alphabetical order as per ImageFolder
CLASS_NAMES = ['Glioma', 'Meningioma', 'No Tumor', 'Pituitary']

uploaded_file = st.file_uploader("Upload an MRI Scan (JPG/PNG)...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display Image
    img = Image.open(uploaded_file).convert('RGB')
    st.image(img, caption='Uploaded MRI', width=300)
    
    # Load model and predict
    model = load_trained_model()
    
    with st.spinner('Analyzing spatial features...'):
        input_tensor = preprocess_image(img)
        with torch.no_grad():
            output = model(input_tensor)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            confidence, predicted_idx = torch.max(probabilities, 0)

    # --- 5. RESULTS DISPLAY ---
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(label="Diagnosis", value=CLASS_NAMES[predicted_idx])
    with col2:
        st.metric(label="Confidence", value=f"{confidence.item()*100:.2f}%")

    # Probability Distribution
    st.write("### Analysis Breakdown")
    for i, name in enumerate(CLASS_NAMES):
        cols = st.columns([2, 8])
        cols[0].write(name)
        cols[1].progress(probabilities[i].item())

st.sidebar.info("Model: EfficientNet-B0 + SE-Attention\nTarget Recall: 99.49%")