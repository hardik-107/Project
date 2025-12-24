import os
import random
import shutil
from tqdm import tqdm

# --- DYNAMIC PATH FIX ---
# Yeh line script ki location ke hisaab se automatic "data" folder dhoond legi
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Agar script "models" folder mein hai, toh ek level upar jaa kar "data" dhoondega
DATA_DIR = os.path.join(BASE_DIR, "..", "data") 

CATEGORIES = ["glioma", "meningioma", "pituitary", "no_tumor"]

def split_dataset(val_ratio=0.15, test_ratio=0.15):
    for cat in CATEGORIES:
        # Full paths with os.path.join for Windows compatibility
        train_path = os.path.abspath(os.path.join(DATA_DIR, "train", cat))
        val_path = os.path.abspath(os.path.join(DATA_DIR, "val", cat))
        test_path = os.path.abspath(os.path.join(DATA_DIR, "test", cat))

        print(f"Checking path: {train_path}") # Debugging ke liye

        if not os.path.exists(train_path):
            print(f"❌ Error: Folder nahi mila -> {train_path}")
            continue

        os.makedirs(val_path, exist_ok=True)
        os.makedirs(test_path, exist_ok=True)

        images = os.listdir(train_path)
        random.shuffle(images)

        val_count = int(len(images) * val_ratio)
        test_count = int(len(images) * test_ratio)

        # Move to Val
        for _ in range(val_count):
            if not images: break
            img = images.pop()
            shutil.move(os.path.join(train_path, img), os.path.join(val_path, img))

        # Move to Test
        for _ in range(test_count):
            if not images: break
            img = images.pop()
            shutil.move(os.path.join(train_path, img), os.path.join(test_path, img))

    print("✅ Data Split Complete!")

if __name__ == "__main__":
    split_dataset()