from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.detect import router as detect_router
from app.api.codehelp import router as codehelp_router
from app.api.lesson import router as lesson_router

app = FastAPI(title="Lumina Backend (stubbed)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # front-end runs on localhost
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include all routers
app.include_router(chat_router)
app.include_router(detect_router)
app.include_router(codehelp_router)
app.include_router(lesson_router)
