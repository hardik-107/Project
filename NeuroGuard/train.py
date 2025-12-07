import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import os
import cv2
import numpy as np
from tqdm import tqdm
from model import DeepfakeDetector

# --- CONFIGURATION (OPTIMIZED) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data/processed_faces")

# Hyperparameters
SEQ_LENGTH = 10     
BATCH_SIZE = 4      # 4GB GPU ke liye safe
EPOCHS = 20         # 20 Epochs ab jaldi honge kyunki CNN freeze hai
LEARNING_RATE = 0.0001
IMG_SIZE = (224, 224)

# --- ROBUST DATASET LOADER ---
class VideoDataset(Dataset):
    def __init__(self, root_dir, sequence_length=10, transform=None):
        self.root_dir = root_dir
        self.sequence_length = sequence_length
        self.transform = transform
        self.video_groups = {}
        
        # Verify directories exist
        if not os.path.exists(root_dir):
            raise RuntimeError(f"Data directory not found: {root_dir}")

        # Scan folders
        for label, category in enumerate(["real", "fake"]):
            cat_path = os.path.join(root_dir, category)
            if not os.path.exists(cat_path):
                print(f"⚠️ Warning: Folder '{category}' not found inside processed_faces!")
                continue
            
            print(f"Scanning {category} images... this might take a moment.")
            files = sorted(os.listdir(cat_path))
            
            # Group images back into videos
            for file in files:
                # Expected format: videoName_f1_0.jpg
                if "_" not in file: continue # Skip junk files
                
                video_name = "_".join(file.split("_")[:-2])
                if video_name not in self.video_groups:
                    self.video_groups[video_name] = []
                self.video_groups[video_name].append((os.path.join(cat_path, file), label))
        
        self.video_list = list(self.video_groups.values())
        print(f"✅ Ready to train on {len(self.video_list)} unique video sequences.")

    def __len__(self):
        return len(self.video_list)

    def __getitem__(self, idx):
        frames_data = self.video_list[idx]
        
        # Safe Sequence Selection
        if len(frames_data) >= self.sequence_length:
            selected_frames = frames_data[:self.sequence_length]
        else:
            # Loop video if too short
            selected_frames = frames_data * (self.sequence_length // len(frames_data) + 1)
            selected_frames = selected_frames[:self.sequence_length]
            
        images = []
        label = selected_frames[0][1] 
        
        for path, _ in selected_frames:
            try:
                img = cv2.imread(path)
                if img is None: raise Exception("Image load failed")
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            except Exception:
                # Fallback: Black frame if image is corrupt (Prevents crashing)
                img = np.zeros((IMG_SIZE[0], IMG_SIZE[1], 3), dtype=np.uint8)
            
            if self.transform:
                img = self.transform(img)
            images.append(img)
            
        # Stack images: (Seq_Len, Channels, Height, Width)
        return torch.stack(images), torch.tensor(label, dtype=torch.float32)

# --- TRAINING ENGINE ---
def train():
    # CUDA Setup
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🔥 Processing Unit: {device}")
    if device.type == 'cuda':
        print(f"   GPU Name: {torch.cuda.get_device_name(0)}")
        torch.backends.cudnn.benchmark = True # Boosts speed for fixed size inputs

    # Data Transforms
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize(IMG_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    # Load Data
    try:
        dataset = VideoDataset(DATA_DIR, sequence_length=SEQ_LENGTH, transform=transform)
    except RuntimeError as e:
        print(f"❌ Error: {e}")
        return

    # Optimized DataLoader (Workers + Pin Memory)
    dataloader = DataLoader(
        dataset, 
        batch_size=BATCH_SIZE, 
        shuffle=True, 
        num_workers=2,      # CPU parallel loading (Windows ke liye 2 safe hai)
        pin_memory=True     # Fast transfer to GPU
    )
    
    # Load Model
    model = DeepfakeDetector(pretrained=True).to(device)
    
    criterion = nn.BCELoss()
    # Optimizer (Sirf un parameters ko update karega jo freeze nahi hain)
    optimizer = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=LEARNING_RATE)

    print(f"🚀 Starting Training for {EPOCHS} Epochs...")
    print("   (Note: First epoch might be slightly slower due to initialization)")
    
    models_dir = os.path.join(BASE_DIR, "../models")
    os.makedirs(models_dir, exist_ok=True)

    for epoch in range(EPOCHS):
        model.train()
        loop = tqdm(dataloader, desc=f"Epoch {epoch+1}/{EPOCHS}")
        epoch_loss = 0
        
        for batch_idx, (videos, labels) in enumerate(loop):
            videos = videos.to(device)
            labels = labels.to(device).unsqueeze(1)
            
            # Forward
            outputs = model(videos)
            loss = criterion(outputs, labels)
            
            # Backward
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            epoch_loss += loss.item()
            loop.set_postfix(loss=loss.item())
            
        # Save Model Every 5 Epochs or Last Epoch
        if (epoch + 1) % 5 == 0 or (epoch + 1) == EPOCHS:
            save_path = os.path.join(models_dir, f"neuroguard_epoch{epoch+1}.pth")
            torch.save(model.state_dict(), save_path)
            print(f"💾 Checkpoint Saved: {save_path}")

    print("✅ Training Complete! Use the last saved model in app.py.")

if __name__ == "__main__":
    train()