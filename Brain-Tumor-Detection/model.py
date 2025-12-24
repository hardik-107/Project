import torch
import torch.nn as nn
from torchvision import models

class BrainTumorModel(nn.Module):
    def __init__(self, num_classes=4):
        super(BrainTumorModel, self).__init__()
        
        # Load Pretrained EfficientNet-B0 (Modern alternative to ResNet)
        self.base_model = models.efficientnet_b0(weights=models.EfficientNet_B0_Weights.DEFAULT)
        
        # Extract features (EfficientNet-B0 outputs 1280 features)
        in_features = self.base_model.classifier[1].in_features
        self.base_model.classifier = nn.Identity()

        # Channel Attention Mechanism (Squeeze-and-Excitation)
        self.attention = nn.Sequential(
            nn.Linear(in_features, in_features // 16),
            nn.ReLU(),
            nn.Linear(in_features // 16, in_features),
            nn.Sigmoid()
        )

        # Final Classification Head
        self.classifier = nn.Sequential(
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        # x shape: (Batch, 3, 224, 224)
        features = self.base_model(x)
        
        # Apply Attention Weights
        att_weights = self.attention(features)
        focused_features = features * att_weights
        
        return self.classifier(focused_features)