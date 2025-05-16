from fastapi import Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from models.schemas import ChatRequest
from models.entities import Project
from utils.llm import llm_response
from models.database import get_db
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

async def chat(query: ChatRequest, db: Session = Depends(get_db)) -> StreamingResponse:
    if not query.query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    query_embedding = embeddings.embed_query(query.query)
    
    similar_projects = db.query(Project).order_by(
        Project.embedding.cosine_distance(query_embedding)
    ).limit(3).all()
    if not similar_projects:
        raise HTTPException(status_code=400, detail="No projects found")
    
    async def stream_res():
        try:
            async for chunk in llm_response(query.query, similar_projects):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: {str(e)}\n\n"
            yield f"data: [DONE]\n\n"
    
    return StreamingResponse(stream_res(), media_type="text/event-stream")