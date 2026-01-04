# 🧠 PixelQuery AI - Semantic Video Search Engine

![PixelQuery Banner](https://via.placeholder.com/1200x400?text=PixelQuery+AI+Preview)
*(Add a screenshot of your UI here later)*

**PixelQuery AI** is a video search engine that allows users to search inside video content using natural language queries. Instead of relying on metadata or tags, it uses **Multimodal AI (OpenAI CLIP)** to understand the visual content of every frame.

Simply upload a video and type *"A red car"* or *"People dancing"*, and the AI will find the exact timestamp.

## 🚀 Features

* **Natural Language Search:** Search video scenes using plain English text.
* **AI-Powered Indexing:** Uses **OpenAI CLIP (ViT-B/32)** to generate vector embeddings for video frames.
* **Smart Frame Extraction:** Optimizes processing by sampling keyframes (1 FPS) using **OpenCV**.
* **GPU Acceleration:** Fully optimized for NVIDIA GPUs (CUDA) for fast inference.
* **Interactive UI:** Modern React frontend with instant "Click-to-Seek" video playback.

## 🛠️ Tech Stack

### Frontend
* **Framework:** React (Vite)
* **Styling:** Tailwind CSS
* **Icons:** Lucide React
* **HTTP Client:** Axios

### Backend
* **Framework:** FastAPI
* **ML Engine:** PyTorch & Transformers
* **Model:** OpenAI CLIP (`ViT-B/32`)
* **Video Processing:** OpenCV (`cv2`)
* **Vector Math:** NumPy

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### Prerequisites
* Python 3.8+
* Node.js & npm
* NVIDIA GPU (Optional, but recommended for speed)


