import torch
import clip
from PIL import Image

# --- 1. SET DEVICE (GPU is Best, CPU is Backup) ---
# Agar NVIDIA GPU hai toh CUDA use hoga, nahi toh CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"🔄 AI Engine Loading on: {device.upper()}...")

# --- 2. LOAD CLIP MODEL (The Professor) ---
# Hum 'ViT-B/32' model use kar rahe hain (Best balance of speed/accuracy)
try:
    model, preprocess = clip.load("ViT-B/32", device=device)
    print("✅ CLIP Model Loaded Successfully!")
except Exception as e:
    print(f"❌ Error Loading CLIP: {e}")
    model = None

# --- 3. TEXT TO VECTOR ---
def get_text_embedding(text: str):
    """
    Input: "A red car"
    Output: [0.1, 0.5, ...] (List of 512 numbers)
    """
    if not model: return None
    
    # Text ko model ke format mein convert karo (Tokenization)
    text_token = clip.tokenize([text]).to(device)
    
    with torch.no_grad():
        # Model se pucho "Iska vector kya hai?"
        text_features = model.encode_text(text_token)
        
    # Vector ko clean karke list banalo (Database ke liye)
    text_features /= text_features.norm(dim=-1, keepdim=True)
    return text_features.cpu().numpy().flatten().tolist()

# --- 4. IMAGE TO VECTOR ---
def get_image_embedding(image_path: str):
    """
    Input: Path to an image file
    Output: Vector list
    """
    if not model: return None
    
    try:
        # Image open karo aur process karo
        image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
        
        with torch.no_grad():
            image_features = model.encode_image(image)
            
        image_features /= image_features.norm(dim=-1, keepdim=True)
        return image_features.cpu().numpy().flatten().tolist()
        
    except Exception as e:
        print(f"⚠️ Error processing image {image_path}: {e}")
        return None