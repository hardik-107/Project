import asyncio
from typing import AsyncIterator
import os

# --- CONFIGURATION ---
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

# --- THE WOVEN DNA (INVISIBLE WATERMARK) ---
# \u200b = Zero Width Space
# \uFEFF = Zero Width No-Break Space
GHOST_DNA = "\u200b\uFEFF"

async def simple_stream_response(system_prompt: str, user_message: str) -> AsyncIterator[str]:
    # (This is the Chat Logic - same as before)
    yield GHOST_DNA

    if HAS_OPENAI:
        try:
            client = OpenAI(
                base_url="http://localhost:11434/v1", 
                api_key="ollama"
            )
            
            stream = client.chat.completions.create(
                model="llama3.2", 
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                stream=True,
            )

            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    yield content
                    if any(char in content for char in [".", "\n", "!", "?", ","]):
                        yield GHOST_DNA
        except Exception as e:
            yield f"Error: Ensure Ollama is running! {str(e)}"
            return
    else:
        yield "Error: Install OpenAI library."

    yield GHOST_DNA

# --- UPDATED CODE GENERATION LOGIC ---
def generate_code_reply(language: str, prompt: str) -> str:
    """
    Generates code and weaves DNA into COMMENTS so it survives copy-paste.
    """
    try:
        # 1. CONNECT TO LOCAL AI
        client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"
        )
        
        # 2. ASK AI FOR CODE
        response = client.chat.completions.create(
            model="llama3.2",
            messages=[
                {"role": "system", "content": "You are a coding assistant. Output ONLY valid code. No markdown, no explanations."},
                {"role": "user", "content": f"Write {language} code for: {prompt}"}
            ]
        )
        code = response.choices[0].message.content or ""

        # 3. WEAVE DNA INTO SYNTAX (The Fix)
        # We replace newlines with a comment containing the DNA.
        
        language = language.lower()
        woven_code = ""
        
        # Python Style Comments (#)
        if "python" in language:
            # Add DNA to every newline
            woven_code = code.replace("\n", f"  # {GHOST_DNA}\n")
            
        # JS/Java/C++ Style Comments (//)
        elif any(x in language for x in ["javascript", "js", "java", "c++", "c", "ts", "typescript"]):
             woven_code = code.replace("\n", f"  // {GHOST_DNA}\n")
        
        # Default (Just wrap it if unknown language)
        else:
             woven_code = f"{GHOST_DNA}\n{code}\n{GHOST_DNA}"

        # Add Start/End markers for good measure
        return f"{GHOST_DNA}{woven_code}{GHOST_DNA}"

    except Exception as e:
        return f"{GHOST_DNA}# Error: Is Ollama running? {str(e)}{GHOST_DNA}"