from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
from app.core.inference import simple_stream_response

router = APIRouter()

class ChatPayload(BaseModel):
    message: str
    system_prompt: str = "You are Lumina AI."

@router.post("/chat/stream")
async def chat_stream(payload: ChatPayload):
    """
    Streaming text response. Frontend reads response.body.getReader() and appends chunks.
    This implementation yields plain text chunks (not SSE) so your current frontend code works.
    """

    async def generator():
        async for chunk in simple_stream_response(payload.system_prompt, payload.message):
            yield chunk

    return StreamingResponse(generator(), media_type="text/plain; charset=utf-8")
