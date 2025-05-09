# ChatDMU API - Requirements Documentation

The ChatDMU API is a FastAPI-based system for managing university graduation projects, user authentication, and admin functionalities. It uses PostgreSQL with pgvector for vector-based similarity searches, JWT for authentication, and integrates with Together AI for conversational project queries via Retrieval-Augmented Generation (RAG).

## Functional Requirements

### User Management

**User Registration**

Register with unique username (alphanumeric, ≥3 characters), email, and password (≥8 characters).
Passwords hashed with bcrypt.
Returns user details; duplicate emails trigger 400 error.


**User Login**

Login with email and password.
Returns JWT token (30-minute expiration).
Incorrect credentials trigger 401 error.



### Admin Management

**Admin Registration**

Only Degree A admins can add admins (Degree A or B).
Requires username, email, password, degree, and added_by field.
Duplicate emails trigger 400 error.


**Admin Login**

Login with email and password.
Returns JWT token (12-hour expiration).
Incorrect credentials trigger 401 error.


**Admin Listing**

Degree A admins can list all admins or filter by degree (A/B).
Returns admin details (ID, username, email, degree, added_by).
Non-Degree A admins trigger 403 error.



### Project Management

**Project Upload**

Admins upload projects with title, supervisor, description, tools (list), and year (2023–current year).
Generates text embedding using all-mpnet-base-v2.
Duplicate titles trigger 500 error.


**Project Retrieval**

Authenticated users retrieve single project by title or all projects.
Returns project details (ID, title, description, tools, supervisor, year).
Non-existent titles trigger 404 error.


**Project Similarity Check**

Check proposed project (title, description) against pre-projects for current academic year.
Uses TF-IDF and cosine similarity; adds project if no matches (score ≤0.5).
Returns similar projects or confirmation.



### Chat Interface

**Project Query Chat**

Users query projects; system retrieves top 3 similar projects via embedding cosine distance.
Processes queries with Llama-3.3-70B (Together API) and streams responses.
Empty queries or no projects trigger 400 error.



## Non-Functional Requirements

### Performance

API endpoints respond within 2 seconds under 100 concurrent users.
Chat streaming responses start within 5 seconds.

### Security

JWT authentication required for all endpoints except registration/login.
Passwords hashed with bcrypt; sensitive data stored in .env.
Invalid tokens trigger 401 error.

### Reliability

99.9% uptime (excluding maintenance).
Graceful error handling with descriptive HTTP status codes (e.g., 400, 500).

### Usability

Clear OpenAPI/Swagger documentation.
Pydantic validation with descriptive error messages.

### Maintainability

Modular codebase (routes, models, auth).
Dependencies listed in requirements.txt; external APIs configurable via .env.

### Compatibility

Runs on PostgreSQL with pgvector and Python 3.8+.
Deployable on localhost (port 5555) or cloud.

## Assumptions and Constraints

### Assumptions

PostgreSQL with pgvector pre-installed.
Environment variables set in .env.


### Constraints

Relies on Together API, risking latency/downtime.
Similarity checks limited to current academic year (October–December increments year).



## Glossary

JWT: JSON Web Token for authentication.
Embedding: Vector representation of text (all-mpnet-base-v2).
pgvector: PostgreSQL extension for vector similarity.
TF-IDF: Term Frequency-Inverse Document Frequency for similarity.
LLM: Large Language Model for chat responses.

