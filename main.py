from fastapi import FastAPI
import uvicorn
from sqlalchemy import text
from app import models
from app.db import engine
from app.routes import router

app=FastAPI()
models.Base.metadata.create_all(bind=engine)

with engine.connect() as connection:
    connection.execute(text("CREATE INDEX IF NOT EXISTS projects_embedding_idx ON projects USING hnsw (embedding vector_cosine_ops)"))
    connection.commit()

app.include_router(router)

if __name__=="__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=5555)

