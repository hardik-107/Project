import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchmetrics.classification import MulticlassF1Score, MulticlassAccuracy, MulticlassPrecision, MulticlassRecall
from tqdm import tqdm
import os

# Import the new architecture from your model.py
from model import BrainTumorModel

# --- DYNAMIC PATH MANAGEMENT ---
# This finds the absolute path of the current script (inside 'models')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# This goes up one level to the project root to find the 'data' folder
DATA_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))

TRAIN_PATH = os.path.join(DATA_ROOT, "train")
VAL_PATH = os.path.join(DATA_ROOT, "val")

# --- CONFIGURATION ---
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BATCH_SIZE = 16  # Optimized for RTX 1650 4GB VRAM
EPOCHS = 15
LEARNING_RATE = 0.0001

# --- DATA AUGMENTATION & LOADERS ---
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Loading datasets using absolute paths
try:
    train_dataset = datasets.ImageFolder(TRAIN_PATH, transform=transform)
    val_dataset = datasets.ImageFolder(VAL_PATH, transform=transform)
    print(f"✅ Data verified at: {DATA_ROOT}")
except FileNotFoundError:
    print(f"❌ Error: Data folder not found at {DATA_ROOT}. Ensure your 'data' folder is in the root directory.")
    exit()

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)

# --- MODEL INITIALIZATION ---
model = BrainTumorModel(num_classes=4).to(DEVICE)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# --- PERFORMANCE METRICS ---
f1_metric = MulticlassF1Score(num_classes=4, average='macro').to(DEVICE)
acc_metric = MulticlassAccuracy(num_classes=4).to(DEVICE)
prec_metric = MulticlassPrecision(num_classes=4, average='macro').to(DEVICE)
rec_metric = MulticlassRecall(num_classes=4, average='macro').to(DEVICE)

# --- TRAINING ENGINE ---
print(f"🚀 Initializing Training Engine on: {DEVICE}")

for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    
    train_bar = tqdm(train_loader, desc=f"Epoch {epoch+1}/{EPOCHS} [Training]")
    for images, labels in train_bar:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
        train_bar.set_postfix(loss=loss.item())

    # --- VALIDATION PHASE ---
    model.eval()
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            preds = model(images)
            
            # Record Performance
            f1_metric.update(preds, labels)
            acc_metric.update(preds, labels)
            prec_metric.update(preds, labels)
            rec_metric.update(preds, labels)
            
    # Final Epoch Report
    print(f"\n📈 Performance Metrics (Epoch {epoch+1}):")
    print(f"Avg Loss:  {running_loss/len(train_loader):.4f}")
    print(f"Accuracy:  {acc_metric.compute():.4f}")
    print(f"F1 Score:  {f1_metric.compute():.4f}")
    print(f"Precision: {prec_metric.compute():.4f}")
    print(f"Recall:    {rec_metric.compute():.4f}") # Critical for medical diagnosis
    
    # Reset for next epoch
    for m in [f1_metric, acc_metric, prec_metric, rec_metric]:
        m.reset()

# --- SAVE FINAL WEIGHTS ---
SAVE_PATH = os.path.join(BASE_DIR, "brain_tumor_attention_v1.pth")
torch.save(model.state_dict(), SAVE_PATH)
print(f"\n🎉 Process Complete. Model saved at: {SAVE_PATH}")