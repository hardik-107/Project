import streamlit as st
import torch
import cv2
import numpy as np
import tempfile
from torchvision import transforms
from model import DeepfakeDetector
import mediapipe as mp
import os

# --- CONFIGURATION ---
MODEL_PATH = "../models/neuroguard_epoch20.pth" 
IMG_SIZE = (224, 224)
SEQ_LENGTH = 10

# --- PAGE SETUP ---
st.set_page_config(page_title="NeuroGuard", page_icon="🛡️", layout="wide")

# --- MIDNIGHT PRO THEME (DARK & RICH) ---
st.markdown("""
    <style>
        /* Force Dark Background */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        
        /* Typography */
        h1, h2, h3 {
            color: #FFFFFF !important;
            font-family: 'SF Pro Display', sans-serif;
            font-weight: 700;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #161B22;
            border-right: 1px solid #30363D;
        }
        
        /* Cards/Containers (Glass Effect) */
        div[data-testid="stMetric"], div.css-1r6slb0 {
            background-color: #1F242D;
            border: 1px solid #30363D;
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        
        /* Buttons - Neon Blue Accent */
        .stButton>button {
            background-color: #2962FF;
            color: white;
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #0039CB;
            box-shadow: 0 0 10px rgba(41, 98, 255, 0.5);
        }
        
        /* File Uploader Fix */
        .stFileUploader {
            background-color: #161B22;
            border-radius: 10px;
            padding: 20px;
            border: 1px dashed #30363D;
        }
        
        /* Metrics Text Color Fix */
        [data-testid="stMetricValue"] {
            color: #FFFFFF !important;
        }
        [data-testid="stMetricLabel"] {
            color: #A0AAB5 !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- MODEL LOADER ---
@st.cache_resource
def load_model():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = DeepfakeDetector(pretrained=False)
    
    try:
        if not os.path.exists(MODEL_PATH):
            return None, device, f"File not found: {MODEL_PATH}"
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        model.to(device)
        model.eval()
        return model, device, "Success"
    except Exception as e:
        return None, device, str(e)

# Load Model
model, device, status = load_model()

if model is None:
    st.error(f"⚠️ System Error: Model failed to load. ({status})")
    st.stop()

# --- SIDEBAR ---
st.sidebar.title("🛡️ NeuroGuard")
st.sidebar.caption("v2.0 • Enterprise Forensics")
st.sidebar.markdown("---")

# Status
st.sidebar.markdown("**System Status**")
if torch.cuda.is_available():
    st.sidebar.success(f"GPU Active: {torch.cuda.get_device_name(0)}")
else:
    st.sidebar.warning("CPU Mode (Limited Performance)")

st.sidebar.markdown("---")
st.sidebar.markdown("**Engine Specs**")
st.sidebar.code("""Arch: ResNet50
Temp: LSTM (2x)
FPS: 30Hz Analysis""")

# --- MAIN INTERFACE ---
col1, col2 = st.columns([1, 5])
with col1:
    st.image("https://img.icons8.com/3d-fluency/94/security-checked.png", width=80)
with col2:
    st.title("Video Authenticator")
    st.markdown("##### 🕵️‍♂️ Advanced Deepfake Detection Engine")

st.markdown("---")

# --- FACE PROCESSING ---
def process_video(video_path):
    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
    cap = cv2.VideoCapture(video_path)
    frames = []
    while len(frames) < SEQ_LENGTH:
        ret, frame = cap.read()
        if not ret: break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(frame_rgb)
        if results.detections:
            detection = results.detections[0]
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
            x, y = max(0, x - 20), max(0, y - 20)
            w, h = min(iw, w + 40), min(ih, h + 40)
            face = frame_rgb[y:y+h, x:x+w]
            if face.size > 0:
                face = cv2.resize(face, IMG_SIZE)
                frames.append(face)
    cap.release()
    face_detection.close()
    if len(frames) == 0: return np.array([])
    while len(frames) < SEQ_LENGTH: frames.append(frames[-1]) 
    return np.array(frames[:SEQ_LENGTH])

# --- UI LOGIC ---
uploaded_file = st.file_uploader("📂 Upload Surveillance or Social Media Footage", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    # Save Temp
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    tfile.write(uploaded_file.read())
    video_path = tfile.name
    
    # Layout: Video Left, Analysis Right
    c1, c2 = st.columns([1, 1])
    
    with c1:
        st.subheader("📺 Input Feed")
        st.video(video_path)
    
    with c2:
        st.subheader("📊 Forensic Analysis")
        analyze = st.button("RUN DIAGNOSTICS", use_container_width=True)
        
        if analyze:
            with st.spinner("🔄 Processing biometric vectors..."):
                raw_frames = process_video(video_path)
                
                if len(raw_frames) == 0:
                    st.error("⚠️ No Face Detected. Try a clearer video.")
                else:
                    # Inference
                    transform = transforms.Compose([
                        transforms.ToPILImage(),
                        transforms.ToTensor(),
                        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
                    ])
                    tensor_frames = [transform(f) for f in raw_frames]
                    input_tensor = torch.stack(tensor_frames).unsqueeze(0).to(device)
                    
                    with torch.no_grad():
                        output = model(input_tensor)
                        probability = output.item()
                    
                    # --- RESULTS ---
                    st.markdown("### Verdict")
                    
                    if probability > 0.50:
                        # FAKE
                        st.error("🚨 MANIPULATED CONTENT")
                        conf = probability * 100
                        st.metric("Confidence Score", f"{conf:.1f}%", delta="High Risk", delta_color="inverse")
                        st.progress(int(conf))
                    else:
                        # REAL
                        st.success("✅ AUTHENTIC FOOTAGE")
                        conf = (1 - probability) * 100
                        st.metric("Authenticity Score", f"{conf:.1f}%", delta="Verified")
                        st.progress(int(conf))
                        
                    # Debug View
                    with st.expander("🛠️ View Internal Attention Frames"):
                        st.image(raw_frames[:5], width=100, caption=["F1", "F2", "F3", "F4", "F5"])