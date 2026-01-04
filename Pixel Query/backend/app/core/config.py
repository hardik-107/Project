import os

# Video save karne ke liye folder path
UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Settings
FRAME_INTERVAL = 30  # Har 30 frames (approx 1 sec) par 1 frame lenge