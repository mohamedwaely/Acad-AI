from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from controllers.chat_controller import chat
from models.schemas import ChatRequest, CheckProject
from models.database import get_db
from services.similarity_service import check_similarity

router = APIRouter()

@router.post("/chat", response_class=StreamingResponse)
async def chat_route(query: ChatRequest, db: Session = Depends(get_db)):
    return await chat(query, db)

@router.post("/check-similarity")
async def check_similarity_route(project: CheckProject, db: Session = Depends(get_db)):
    return check_similarity(project, db)