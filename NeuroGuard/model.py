import torch
import torch.nn as nn
from torchvision import models

class DeepfakeDetector(nn.Module):
    def __init__(self, num_classes=1, hidden_dim=128, lstm_layers=2, pretrained=True):
        super(DeepfakeDetector, self).__init__()
        
        # 1. CNN (ResNet50) - Pretrained ImageNet weights
        print("Loading ResNet50... (Weights Frozen for Speed)")
        resnet = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1 if pretrained else None)
        
        # --- SPEED OPTIMIZATION (FREEZING) ---
        # CNN ke weights lock kar rahe hain taaki GPU pe load kam pade
        # Isse training 5x-10x fast ho jayegi aur accuracy badhegi (Transfer Learning)
        for param in resnet.parameters():
            param.requires_grad = False
        # -------------------------------------
        
        # Last layer hatao (Classification nahi, features chahiye)
        modules = list(resnet.children())[:-1] 
        self.cnn = nn.Sequential(*modules)
        
        # ResNet50 ka output size
        self.cnn_output_dim = 2048

        # 2. LSTM (Temporal - Sirf ye train hoga)
        self.lstm = nn.LSTM(
            input_size=self.cnn_output_dim,
            hidden_size=hidden_dim,
            num_layers=lstm_layers,
            batch_first=True,
            dropout=0.3
        )
        
        # 3. Classifier
        self.fc = nn.Linear(hidden_dim, num_classes)
        self.sigmoid = nn.Sigmoid() 

    def forward(self, x):
        # Input: (Batch, Sequence, Channels, Height, Width)
        batch_size, seq_len, c, h, w = x.size()
        
        # CNN Process (Fast mode because gradients are off)
        c_in = x.view(batch_size * seq_len, c, h, w)
        cnn_out = self.cnn(c_in) # Output: (Batch*Seq, 2048, 1, 1)
        
        # Sequence mein wapas todo
        lstm_in = cnn_out.view(batch_size, seq_len, -1)
        
        # LSTM run karo
        lstm_out, _ = self.lstm(lstm_in)
        
        # Last frame ke features lo
        last_frame_features = lstm_out[:, -1, :] 
        
        logits = self.fc(last_frame_features)
        probability = self.sigmoid(logits)
        
        return probability