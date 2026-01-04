from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import numpy as np
from app.core.config import UPLOAD_DIR
from app.services.video_processor import video_engine
from app.services.ai_engine import model, preprocess, device, get_text_embedding
import torch
from PIL import Image

router = APIRouter()

# --- IN-MEMORY DATABASE ---
# Asli project mein hum FAISS use karenge, abhi ke liye RAM use karte hain
# Structure: [{"timestamp": 1.5, "vector": [0.1, ...]}, ...]
VIDEO_INDEX = []

@router.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    global VIDEO_INDEX
    
    # 1. Video Save karo
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 2. Frames Nikalo
        print(f"📂 Processing: {file.filename}")
        frames_data = video_engine.extract_keyframes(file_path)
        
        # 3. Database Clear karo (Nayi video ke liye)
        VIDEO_INDEX = [] 

        print(f"🧠 Generating Vectors for {len(frames_data)} frames...")
        
        # 4. Vectors Generate Karo
        for item in frames_data:
            pil_image = Image.fromarray(item["frame"])
            
            # Image to Vector
            image_input = preprocess(pil_image).unsqueeze(0).to(device)
            with torch.no_grad():
                image_features = model.encode_image(image_input)
                # Normalize (Zaroori hai matching ke liye)
                image_features /= image_features.norm(dim=-1, keepdim=True)
            
            VIDEO_INDEX.append({
                "timestamp": item["timestamp"],
                "vector": image_features.cpu().numpy() # Store as Numpy array
            })

        return {
            "status": "success", 
            "message": f"Video Processed! {len(VIDEO_INDEX)} scenes ready for search.",
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
    
    finally:
        video_engine.cleanup(file_path)

@router.get("/search")
async def search_video(query: str):
    """
    User: "Find a red car"
    AI: Maths lagake best timestamp dhundega.
    """
    if not VIDEO_INDEX:
        return {"error": "No video uploaded yet!"}

    print(f"🔍 Searching for: {query}")
    
    # 1. Text ko Vector banao
    text_vec = get_text_embedding(query) # Returns list
    text_vec_np = np.array(text_vec).reshape(1, -1) # Convert to Numpy shape (1, 512)

    results = []

    # 2. Har frame se compare karo (Dot Product)
    for entry in VIDEO_INDEX:
        frame_vec = entry["vector"] # Shape (1, 512)
        
        # Similarity Score (Jitna high, utna match)
        # (A . B) formula
        score = np.dot(text_vec_np, frame_vec.T)[0][0]
        
        results.append({
            "timestamp": entry["timestamp"],
            "score": float(score)
        })

    # 3. Sort karo (Highest score upar)
    results.sort(key=lambda x: x["score"], reverse=True)

    # Top 3 Matches return karo
    return {"matches": results[:3]}