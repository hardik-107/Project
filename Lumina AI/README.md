# Lumina AI: Generative Content Authentication System

![Python](https://img.shields.io/badge/Backend-FastAPI-009688)
![React](https://img.shields.io/badge/Frontend-React-61DAFB)
![License](https://img.shields.io/badge/License-MIT-blue)

Lumina AI is a full-stack forensic application designed to verify the authenticity of digital content. It addresses the challenge of distinguishing between human-authored and AI-generated text through statistical linguistic analysis and implements a proprietary watermarking protocol ("GhostPrint") for content traceability.

## Project Overview

The system operates on a dual-layer architecture:
1.  **Detection Engine:** Analyzes text inputs for statistical anomalies typical of Large Language Models (LLMs), specifically focusing on Perplexity and Burstiness metrics.
2.  **Watermarking Engine:** Injects non-printing zero-width characters into generated outputs to create an immutable digital signature for provenance tracking.

## Technical Capabilities

### 1. GhostPrint Detection Engine
The core detection module utilizes a hybrid approach:
* **Heuristic Analysis:** Calculates probability scores based on linguistic variance. High uniformity indicates AI generation, while high variance indicates human authorship.
* **Watermark Verification:** Scans for specific Unicode markers (`\u200b`, `\uFEFF`) to provide 100% certainty for content generated within the Lumina ecosystem.

### 2. Secure Code Generation
* **Traceability:** Automatically injects invisible markers into code comments during generation. This allows organizations to track code provenance even after it has been copied and pasted into IDEs.
* **Syntax Awareness:** The injection logic adapts to different commenting syntaxes (e.g., `#` for Python, `//` for JavaScript) to ensure code remains valid and executable.

### 3. Voice-Enabled Interface
* **Streaming Architecture:** Implements Server-Sent Events (SSE) logic via FastAPI for real-time token streaming.
* **Bi-directional Audio:** Integrates the Web Speech API for voice-to-text input and SpeechSynthesis for text-to-speech output.

## Technical Stack

| Component | Technology |
| :--- | :--- |
| **Backend Framework** | FastAPI (Python 3.10+) |
| **Frontend Framework** | React.js (Vite Build Tool) |
| **AI Inference** | Ollama (Llama 3.2), OpenAI API Protocol |
| **State Management** | React Hooks |
| **Data Processing** | NumPy, Pydantic |

## Project Structure

The repository is structured as a decoupled monorepo:

```bash
Lumina-AI/
├── backend/
│   ├── main.py           # Application entry point and routing
│   ├── ghostprint.py     # Core detection logic and heuristics
│   ├── inference.py      # LLM interaction and stream handling
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/   # Modular React components (Chat, Detect, Code)
│   │   └── App.jsx       # Client-side routing and layout

│   └── package.json      # Frontend dependencies

## Installation and Deployment

Follow these steps to set up the environment locally.

### Prerequisites

Ensure the following tools are installed on your system:
* **Python 3.10+**
* **Node.js** (v16 or higher) and npm
* **Ollama** (for local LLM inference)

### 1. Repository Setup

Clone the repository and navigate to the project root:

```bash
git clone [https://github.com/yourusername/Lumina-AI.git](https://github.com/yourusername/Lumina-AI.git)
cd Lumina-AI

cd backend

# Install dependencies
pip install -r requirements.txt

# Start the API server
uvicorn main:app --reload

cd frontend

# Install Node modules
npm install

# Launch the development server
npm run dev

# Pull the model (run this once)
ollama pull llama3.2

# Serve the model
ollama serve
