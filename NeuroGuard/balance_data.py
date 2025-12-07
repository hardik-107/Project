import os
import random
from tqdm import tqdm

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "../data/processed_faces")

def balance_dataset():
    real_dir = os.path.join(DATA_DIR, "real")
    fake_dir = os.path.join(DATA_DIR, "fake")
    
    # 1. Count files
    real_files = os.listdir(real_dir)
    fake_files = os.listdir(fake_dir)
    
    count_real = len(real_files)
    count_fake = len(fake_files)
    
    print(f"Real Images: {count_real}")
    print(f"Fake Images: {count_fake}")
    
    if count_fake <= count_real:
        print("✅ Data is already balanced (or Real > Fake). No action needed.")
        return

    # 2. Calculate how many to delete
    # We keep slightly more fakes (e.g. 1.0x) to be safe, or exactly equal.
    target_count = count_real 
    files_to_delete = count_fake - target_count
    
    print(f"⚠️ Imbalance detected! Need to delete {files_to_delete} fake images...")
    print("Deleting randomly to balance datasets...")
    
    # 3. Shuffle and Delete
    random.shuffle(fake_files)
    files_to_remove = fake_files[:files_to_delete]
    
    for f in tqdm(files_to_remove):
        file_path = os.path.join(fake_dir, f)
        os.remove(file_path)
        
    print(f"✅ Cleanup Complete! Now you have:")
    print(f"Real: {len(os.listdir(real_dir))}")
    print(f"Fake: {len(os.listdir(fake_dir))}")
    print("🚀 You can now retrain your model!")

if __name__ == "__main__":
    balance_dataset()