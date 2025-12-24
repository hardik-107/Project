import torch
import os
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchmetrics.classification import MulticlassF1Score, MulticlassAccuracy, MulticlassRecall
from model import BrainTumorModel # Import your specific architecture

# 1. Setup Device and Paths
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "brain_tumor_attention_v1.pth")
TEST_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "data", "test"))

# 2. Define Model and Load Weights
model = BrainTumorModel(num_classes=4).to(DEVICE)
if os.path.exists(MODEL_PATH):
    model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
    print(f"✅ Loaded weights from: {MODEL_PATH}")
else:
    print(f"❌ Error: Weights file not found at {MODEL_PATH}")
    exit()

# 3. Data Loader for Test Set
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

test_dataset = datasets.ImageFolder(TEST_PATH, transform=transform)
test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)

# 4. Initialize Metrics
f1_metric = MulticlassF1Score(num_classes=4, average='macro').to(DEVICE)
acc_metric = MulticlassAccuracy(num_classes=4).to(DEVICE)
rec_metric = MulticlassRecall(num_classes=4, average='macro').to(DEVICE)

# 5. Evaluation Loop
print(f"🚀 Starting final evaluation on Test Set...")
model.eval()
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        preds = model(images)
        
        f1_metric.update(preds, labels)
        acc_metric.update(preds, labels)
        rec_metric.update(preds, labels)

# 6. Final Results for Resume
print("\n" + "="*30)
print("FINAL TEST RESULTS")
print("="*30)
print(f"Final Accuracy:  {acc_metric.compute():.4f}")
print(f"Final F1 Score:  {f1_metric.compute():.4f}")
print(f"Final Recall:    {rec_metric.compute():.4f}") # Critical for medical AI
print("="*30)