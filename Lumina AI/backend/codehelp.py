from fastapi import APIRouter
from pydantic import BaseModel
from app.core.inference import generate_code_reply

router = APIRouter(prefix="/api")

class CodeHelpRequest(BaseModel):
    language: str
    prompt: str

@router.post("/codehelp")
def codehelp(payload: CodeHelpRequest):
    """
    Basic code generation/stub endpoint.
    Returns { reply: "...code or explanation..." }
    """
    reply = generate_code_reply(payload.language or "python", payload.prompt)
    return {"reply": reply}
