# Autonomous Local Text-to-SQL Agent

## Overview
This repository contains an end-to-end, privacy-centric AI agent capable of translating natural language questions into executable SQL queries. The system is built using a fine-tuned Llama-3 (8B) model integrated with LangChain to autonomously query a local SQLite database and return precise answers. 

The entire pipeline is optimized for edge computing, enabling full offline inference on resource-constrained hardware (e.g., 4GB VRAM) without relying on external APIs.

## Key Features
* **Local & Private Inference:** Operates 100% offline, ensuring zero data leakage to third-party cloud services.
* **Custom LLM Fine-Tuning:** Utilizes QLoRA (4-bit quantization) to fine-tune the Llama-3 model specifically for SQL syntax and schema adherence, minimizing hallucinations.
* **Autonomous Execution:** Implements a LangChain pipeline that reads database schemas, generates SQL, executes the query, and parses the final result automatically.
* **Hardware Optimization:** Configured with `bitsandbytes` and `peft` to manage memory efficiently during both training and inference on limited GPU architectures.

## Technology Stack
* **Language:** Python 3.11
* **Large Language Model:** Llama-3 (8B)
* **Frameworks & Libraries:** LangChain, HuggingFace (Transformers, Peft, Accelerate), PyTorch
* **Database:** SQLite
* **Quantization:** bitsandbytes (4-bit)

## Project Structure
* `src/`
  * `01_data_generator.py`: Generates synthetic data and schemas for training.
  * `02_train_qlora.py`: Script for fine-tuning the base model using QLoRA.
  * `03_evaluator.py`: Evaluates model performance and SQL accuracy.
  * `04_langchain_agent.py`: The main execution script running the LangChain autonomous pipeline.
* `data/`: Contains the SQLite database (`company_data.db`) and synthetic query logs.
* `models/qlora_adapters/`: Contains the fine-tuned adapter configurations and tokenizers.

## Installation & Setup

1. **Clone the repository and navigate to the project folder:**
   ```bash
   git clone [https://github.com/hardik-107/Project.git](https://github.com/hardik-107/Project.git)
   cd Project/"Text To SQL Agent"
