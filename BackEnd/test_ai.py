import os
from dotenv import load_dotenv
from importlib import import_module
from openai import OpenAI
from openai import AsyncOpenAI

from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app = FastAPI()
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Use ["*"] to allow all origins during testing
    allow_credentials=True,
    allow_methods=["*"],    # Allows all methods, including OPTIONS, GET, POST, etc.
    allow_headers=["*"],    # Allows all headers
)


client = AsyncOpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

response = client.chat.completions.create(
    model=os.getenv("NVIDIA_MODEL"),
    messages=[
        {
            "role":"user", 
            "content": "Explain what is Python in simple words."
        }
    ],
    max_tokens=200
)

#print(response.choices[0].message.content)

class ChatRequest(BaseModel):
    question: str
@app.post("/api/chat")
async def chat(request: ChatRequest):
    print(request.question)
    #return{"answer":"Lots OF Rain"}
    
    response = await client.chat.completions.create(
        model=os.getenv("NVIDIA_MODEL"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant for students."},
            {"role": "user", "content": request.question}
        ],
        max_tokens=300
    )
    return {"answer": response.choices[0].message.content or ""}