from fastapi import FastAPI
import uvicorn
from sqlalchemy import text
from models.entities import Base
from models.database import engine
from routes.auth_routes import router as auth_router
from routes.project_routes import router as project_router
from routes.admin_routes import router as admin_router
from routes.chat_routes import router as chat_router
from utils.metrics import setup_metrics


app = FastAPI()

#setup prometheus metrics
setup_metrics(app)

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

# Create vector index for embeddings
try:
    with engine.connect() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        connection.execute(text("CREATE INDEX IF NOT EXISTS projects_embedding_idx ON projects USING hnsw (embedding vector_cosine_ops)"))
        connection.commit()
except Exception as e:
    print(f"Warning: Could not create vector index. This is expected if running for the first time: {e}")

# Include routers
app.include_router(auth_router, prefix="/v1")
app.include_router(project_router, prefix="/v1")
app.include_router(admin_router, prefix="/v1")
app.include_router(chat_router, prefix="/v1")

if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=5555)

