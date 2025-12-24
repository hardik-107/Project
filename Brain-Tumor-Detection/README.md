Brain Tumor Diagnostic Engine (Attention-Based CNN)This project is a high-precision medical imaging solution designed to classify four types of brain conditions from MRI scans: Glioma, Meningioma, Pituitary Tumor, and No Tumor. Developed during my B.Tech IT Final Year (2026), it focuses on high-reliability clinical diagnostics2222.🚀 Key FeaturesModern Architecture: Utilizes EfficientNet-B0 as the backbone for superior feature extraction with fewer parameters.Attention Mechanism: Implemented Squeeze-and-Excitation (SE) Attention blocks to help the model focus on subtle pathological textures in MRI slices.High-Reliability Metrics: Optimized for Recall (99.49%) to minimize False Negatives, ensuring critical tumors are not missed during screening.Interactive Deployment: Includes a Streamlit dashboard for real-time inference, displaying probability distributions and confidence scores.🛠️ Tech StackLanguage: Python 3Deep Learning Framework: PyTorch & TorchvisionArchitecture: EfficientNet-B0 + SE-AttentionHardware Acceleration: NVIDIA CUDA (Optimized for RTX 1650)Dashboard: Streamlit📊 Performance SummaryAfter 15 epochs of training, the model achieved the following results on the hold-out test set:MetricScoreAccuracy99.49%Recall (Sensitivity)99.49%F1-Score99.42%Precision99.36%📁 Project StructurePlaintextBrain-Tumor-Detection/
├── data/               # Stratified Train/Val/Test Split
├── models/
│   ├── train.py        # Optimized training engine
│   ├── model.py        # EfficientNet + Attention architecture
│   └── *.pth           # Trained weights (99% Accuracy)
├── app.py              # Streamlit Web Dashboard
└── README.md
🔧 How to RunInstall Dependencies:Bashpip install torch torchvision streamlit tqdm torchmetrics pillow
Run Training (Optional):Bashpython models/train.py
Launch Dashboard:Bashstreamlit run app.py
🤝 Comparison with NeuroGuardWhile my previous project, NeuroGuard, focused on temporal anomalies in video sequences using ResNet50 + LSTM4, this project addresses spatial pathology in static medical imagery using Attention Mechanisms to improve diagnostic precision.