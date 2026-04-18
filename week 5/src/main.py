from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import uvicorn
import os
import sys

# Setup paths
base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)

# Week 4 integration
week4_src = os.path.join(base_dir, '..', '..', 'week 4', 'src')
sys.path.append(week4_src)

from auth.jwt_handler import create_access_token
from database.database import get_db, User, pwd_context
from sqlalchemy.orm import Session
from middleware.rbac_middleware import RoleChecker

# Search & RAG Pipeline
try:
    from search_pipeline import SearchPipeline
    # Import RAG from week 6
    sys.path.append(os.path.join(base_dir, '..', '..', 'week 6', 'src'))
    from rag_pipeline import RAGPipeline
    
    # Initialize RAG (which initializes Search internally)
    rag = RAGPipeline()
except ImportError as e:
    print(f"Warning: Pipeline not found: {e}")
    rag = None

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RBAC Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class QueryRequest(BaseModel):
    query: str

# Endpoints

@app.post("/auth/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user or not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    
    access_token = create_access_token(user_id=str(user.id), role=user.role)
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "role": user.role,  # Include role in response
        "username": user.username
    }

@app.post("/query/finance")
def query_finance(request: QueryRequest, user: dict = Depends(RoleChecker(["finance", "c-level"]))):
    if not rag: return {"error": "RAG unavailable"}
    return rag.generate_response(request.query, user["role"])

@app.post("/query/hr")
def query_hr(request: QueryRequest, user: dict = Depends(RoleChecker(["hr", "c-level"]))):
    if not rag: return {"error": "RAG unavailable"}
    return rag.generate_response(request.query, user["role"])

@app.post("/query/marketing")
def query_marketing(request: QueryRequest, user: dict = Depends(RoleChecker(["marketing", "c-level"]))):
    if not rag: return {"error": "RAG unavailable"}
    return rag.generate_response(request.query, user["role"])

@app.post("/query/engineering")
def query_engineering(request: QueryRequest, user: dict = Depends(RoleChecker(["engineering", "c-level"]))):
    if not rag: return {"error": "RAG unavailable"}
    return rag.generate_response(request.query, user["role"])

@app.post("/query/general")
def query_general(request: QueryRequest, user: dict = Depends(RoleChecker(["employees", "finance", "hr", "marketing", "engineering", "c-level"]))):
    if not rag: return {"error": "RAG unavailable"}
    return rag.generate_response(request.query, user["role"])

# Health Check
@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "RBAC Chatbot API is running. Go to /docs for Swagger UI."}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
