import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from google import genai
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not found. Please set it in .env")

# Initialize Gemini Client
client = genai.Client(api_key=api_key)

app = FastAPI(
    title="Chatbot Service API",
    description="A REST API for interacting with the Gemini AI chatbot for internship submission.",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    message: str = Field(..., example="What is an API?")
    system_instruction: str | None = Field(
        default="You are a helpful and polite technical AI assistant.",
        example="You are a senior developer helping an intern."
    )

class ChatResponse(BaseModel):
    status: str
    response: str

@app.get("/")
def read_root():
    return {"status": "online", "message": "Chatbot API is running successfully."}

@app.post("/api/v1/chat", response_model=ChatResponse)
def generate_chat_response(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        api_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.message,
            config={
                "system_instruction": request.system_instruction
            }
        )
        return ChatResponse(status="success", response=api_response.text)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Service Error: {str(e)}")