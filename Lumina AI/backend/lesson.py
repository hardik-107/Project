from fastapi import APIRouter
from pydantic import BaseModel
import json

try:
    from openai import OpenAI
    HAS_AI = True
except ImportError:
    HAS_AI = False

router = APIRouter(prefix="/api")

# --- DATA MODELS ---
class LessonRequest(BaseModel):
    topic: str

class CheckRequest(BaseModel):
    exercise_prompt: str
    user_code: str

# --- 1. GENERATE LESSON (Existing) ---
@router.post("/lesson")
def lesson(payload: LessonRequest):
    topic = payload.topic or "Python Basics"
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

    system_prompt = (
        "You are an expert Python Tutor. Create a short lesson. "
        "Format exactly:\nTITLE: <Title>\nCONTENT: <Explanation>\nEXERCISE: <Coding Challenge>"
    )

    try:
        response = client.chat.completions.create(
            model="llama3.2", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Teach: {topic}"}
            ]
        )
        text = response.choices[0].message.content
        
        # Robust Parsing
        title = f"Lesson: {topic}"
        content = text
        exercise = "See content."

        if "TITLE:" in text and "CONTENT:" in text:
            try:
                parts_after_title = text.split("TITLE:", 1)[1]
                title_part, rest = parts_after_title.split("CONTENT:", 1)
                title = title_part.strip()
                if "EXERCISE:" in rest:
                    content_part, exercise_part = rest.split("EXERCISE:", 1)
                    content = content_part.strip()
                    exercise = exercise_part.strip()
                else:
                    content = rest.strip()
            except:
                pass

        return {"lesson": {"title": title, "content": content, "exercise": exercise}}

    except Exception as e:
        return {"lesson": {"title": "Error", "content": str(e), "exercise": ""}}


# --- 2. CHECK STUDENT CODE (New Feature) ---
@router.post("/check_exercise")
def check_exercise(payload: CheckRequest):
    """
    Analyzes the student's code against the exercise.
    Returns feedback, finding syntax errors or logic mistakes.
    """
    client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

    # The AI acts as a grader
    system_prompt = (
        "You are a friendly Code Mentor. "
        "The student has submitted code for a Python challenge. "
        "Analyze their code for syntax errors, logic flaws, or correctness. "
        "Be encouraging but precise. "
        "If it is correct, say 'PASS'. If incorrect, explain why."
    )

    user_prompt = (
        f"CHALLENGE: {payload.exercise_prompt}\n"
        f"STUDENT CODE:\n{payload.user_code}\n\n"
        "Give short, helpful feedback."
    )

    try:
        response = client.chat.completions.create(
            model="llama3.2",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        feedback = response.choices[0].message.content
        return {"feedback": feedback}
    
    except Exception as e:
        return {"feedback": f"Error checking code: {str(e)}"}