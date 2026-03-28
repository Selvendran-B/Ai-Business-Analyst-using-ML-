from fastapi import APIRouter
from backend.services.ai_agent import BusinessAgent

router = APIRouter()
agent = BusinessAgent()

@router.get("/ask")
def ask_agent(q: str):
    return {"answer": agent.answer(q)}
