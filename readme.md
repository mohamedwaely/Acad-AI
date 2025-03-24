# ChatDMU API - Project Management and Chat System

ChatDMU API is an intelligent project management system that leverages Retrieval-Augmented Generation (RAG) to provide conversational access to university graduation projects, user authentication, and admin management.

Anyone can chat with the AI about projects through RAG, and only admins can upload new projects. Admins can also add new admins, and only admins with the Degree A role can add new admins with the Degree B role.

## Features

- **User Authentication**
  - Secure JWT token-based authentication
  - Role-based access control (User/Admin)
  - Password hashing with bcrypt

- **Admin Management**
  - Hierarchical admin roles (Degree A/B)
  - Admin creation restricted to higher-level admins

- **Project Management**
  - Project upload with metadata
  - Vector embeddings for semantic search
  - HNSW indexing for efficient similarity search

- **AI Chat System**
  - Context-aware responses about projects
  - Together AI integration for intelligent Q&A
  - Project recommendations based on queries

## Built With

**Backend:**
- [FastAPI](https://fastapi.tiangolo.com/) - Python web framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM for PostgreSQL
- [pgvector](https://github.com/pgvector/pgvector) - Vector similarity search

**Authentication:**
- [JOSE/JWT](https://python-jose.readthedocs.io/) - Token authentication
- [Passlib](https://passlib.readthedocs.io/) - Password hashing (bcrypt)

**AI/ML:**
- [HuggingFace](https://huggingface.co/) - Sentence Transformers (all-mpnet-base-v2)
- [Together AI](https://api.together.ai) - LLM chat completions with streaming responses
- [LangChain](https://python.langchain.com/) - Embedding pipeline

**Database:**
- [PostgreSQL](https://www.postgresql.org/) - primary database with pgvector Extension to allow vector similarity search
- [HNSW](https://github.com/pgvector/pgvector#hnsw) - Approximate nearest neighbor index

## API Endpoints

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/v1/register` | POST | User registration | No |
| `/v1/token` | POST | Login (JWT token generation) | No |
| `/v1/add-admin` | POST | Add new admin | Admin (Degree A) |
| `/v1/upload-projects` | POST | Upload new project | Admin |
| `/v1/chat` | POST | AI chat about projects | No |

## Setup
1. Install requirements: `pip install -r requirements.txt`
2. Configure environment variables
3. Run: `python main.py`