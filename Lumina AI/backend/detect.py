from fastapi import APIRouter
from pydantic import BaseModel
from app.core.ghostprint import detect_ai

router = APIRouter(prefix="/api")

class DetectRequest(BaseModel):
    text: str

@router.post("/detect")
def detect(payload: DetectRequest):
    """
    Returns a JSON analysis of whether input text is AI-generated.
    """
    return detect_ai(payload.text)
