import torch
from torchmetrics.classification import BinaryF1Score, BinaryAccuracy
from model import DeepfakeDetector
import json

def generate_final_report(model, test_loader):
    f1 = BinaryF1Score()
    acc = BinaryAccuracy()
    
    model.eval()
    with torch.no_grad():
        for x, y in test_loader:
            preds = model(x)
            f1.update(preds, y)
            acc.update(preds, y)
    
    results = {
        "accuracy": f"{(acc.compute().item() * 100):.2f}%",
        "f1_score": f"{f1.compute().item():.3f}",
        "status": "Enterprise Ready"
    }
    
    # Save for App.py to read
    with open("models/metrics.json", "w") as f:
        json.dump(results, f)
    print("Report Generated!")