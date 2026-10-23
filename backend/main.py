
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from agent import answer_question
from rag import build_index

app = FastAPI(
    title="AsEl-AI Healthcare Support Agent",
    description=(
        "A prototype for answering healthcare support questions "
        "using fictional policies and synthetic appointment data."
    ),
    version="1.0.0",
)


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=2,
        max_length=1000,
        description="A healthcare support question",
    )


class ChatResponse(BaseModel):
    answer: str


# Build the policy search index once when the API starts.
collection, model = build_index()


@app.get("/")
def home():
    return {
        "message": "AsEl-AI Healthcare Support Agent API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        answer = answer_question(request.question, collection, model)
        return ChatResponse(answer=answer)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="The agent could not process this question.",
        )
