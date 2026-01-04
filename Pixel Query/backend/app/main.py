from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# --- DIRECT IMPORT (No Try-Except) ---
# Agar yahan error aaya, toh Terminal mein crash hoga aur humein reason dikhega
from app.api import endpoints

app = FastAPI(title="PixelQuery Backend")

# --- CORS SETUP ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- REGISTER ROUTES ---
app.include_router(endpoints.router)

@app.get("/")
def home():
    return {"message": "PixelQuery is Ready 🧠"}