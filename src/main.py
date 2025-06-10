from fastapi import FastAPI
import uvicorn
from sqlalchemy import text
from models.entities import Base
from models.database import engine
from routes.auth_routes import router as auth_router
from routes.project_routes import router as project_router
from routes.admin_routes import router as admin_router
from routes.chat_routes import router as chat_router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="Project Management API",
    description="FastAPI application for project management and AI chat",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080", 
        "https://*.vercel.app",
        "https://*.netlify.app",
        "*"  # Remove this in production
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Health check first (before DB operations)
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/")
async def root():
    return {
        "message": "Project Management API is running!",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Create tables if they don't exist
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")
except Exception as e:
    print(f"Database table creation warning: {e}")

# Create vector index for embeddings
try:
    with engine.connect() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        connection.execute(text("CREATE INDEX IF NOT EXISTS projects_embedding_idx ON projects USING hnsw (embedding vector_cosine_ops)"))
        connection.commit()
        print("Vector extension and index created successfully")
except Exception as e:
    print(f"Vector extension warning: {e}")

# Include routers
app.include_router(auth_router, prefix="/v1", tags=["Authentication"])
app.include_router(project_router, prefix="/v1", tags=["Projects"])
app.include_router(admin_router, prefix="/v1", tags=["Admin"])
app.include_router(chat_router, prefix="/v1", tags=["Chat"])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app=app, host="0.0.0.0", port=port)
