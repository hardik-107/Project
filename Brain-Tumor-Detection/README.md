# 🧠 Brain Tumor Diagnostic Engine
> **High-Precision MRI Classification using Attention-Augmented EfficientNet-B0**

## 📊 Performance at a Glance
To ensure patient safety, the model was optimized to minimize False Negatives.

| Metric | Value |
| :--- | :--- |
| **Accuracy** | **99.49%** |
| **Recall (Sensitivity)** | **99.49%** |
| **F1-Score** | **99.42%** |



---

## 🛠️ Technical Architecture
Unlike standard CNNs, this model uses an **Attention Mechanism** to focus on subtle textures in MRI slices.

* **Backbone:** EfficientNet-B0 (Pre-trained on ImageNet).
* **Attention:** Squeeze-and-Excitation (SE) Blocks for spatial feature recalibration.
* **Optimization:** Cross-Entropy Loss with Adam Optimizer.



---

## 🖥️ Streamlit Dashboard
The deployment features a professional dashboard for real-time diagnostics:
* **MRI Upload:** Supports JPG, PNG, and JPEG.
* **Probability Distribution:** Visualizes the model's confidence across all 4 classes.
* **Explainable UI:** Designed for high-resolution medical image analysis.

---

## 📁 Installation & Usage
1. **Clone the Repo:**
   ```bash
   git clone [https://github.com/hardik-107/Brain-Tumor-Detection.git](https://github.com/hardik-107/Brain-Tumor-Detection.git)
