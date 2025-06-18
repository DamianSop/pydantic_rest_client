#!/usr/bin/env python3
"""
Simple FastAPI test server for testing pydantic-rest-client
Run this server to test HTTP requests locally
"""

import uvicorn
from fastapi import FastAPI, HTTPException, status, Request
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

# Create FastAPI app
app = FastAPI(
    title="Test API for pydantic-rest-client",
    description="A simple API for testing HTTP requests",
    version="1.0.0"
)

# Data models
class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    avatar: str

class UserResponse(BaseModel):
    data: User

class CreateUserRequest(BaseModel):
    name: str
    job: str

class CreateUserResponse(BaseModel):
    name: str
    job: str
    id: str
    created_at: str

class UpdateUserRequest(BaseModel):
    name: Optional[str] = None
    job: Optional[str] = None

# In-memory storage
users_db = {
    1: User(id=1, first_name="George", last_name="Bluth", email="george.bluth@reqres.in", avatar="https://reqres.in/img/faces/1-image.jpg"),
    2: User(id=2, first_name="Janet", last_name="Weaver", email="janet.weaver@reqres.in", avatar="https://reqres.in/img/faces/2-image.jpg"),
    3: User(id=3, first_name="Emma", last_name="Wong", email="emma.wong@reqres.in", avatar="https://reqres.in/img/faces/3-image.jpg"),
}

created_users = {}

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Test API for pydantic-rest-client", "version": "1.0.0"}

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Get user by ID"""
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(data=users_db[user_id])

@app.get("/users", response_model=List[UserResponse])
async def get_users():
    """Get all users"""
    return [UserResponse(data=user) for user in users_db.values()]

@app.post("/users", response_model=CreateUserResponse, status_code=201)
async def create_user(user: CreateUserRequest):
    """Create a new user"""
    user_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    
    created_users[user_id] = CreateUserResponse(
        name=user.name,
        job=user.job,
        id=user_id,
        created_at=created_at
    )
    
    return created_users[user_id]

@app.put("/users/{user_id}", response_model=CreateUserResponse)
async def update_user(user_id: str, user: CreateUserRequest):
    """Update user by ID"""
    if user_id not in created_users:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = CreateUserResponse(
        name=user.name,
        job=user.job,
        id=user_id,
        created_at=created_users[user_id].created_at
    )
    created_users[user_id] = updated_user
    
    return updated_user

@app.patch("/users/{user_id}", response_model=CreateUserResponse)
async def patch_user(user_id: str, user: UpdateUserRequest):
    """Partially update user by ID"""
    if user_id not in created_users:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_user = created_users[user_id]
    updated_user = CreateUserResponse(
        name=user.name if user.name is not None else current_user.name,
        job=user.job if user.job is not None else current_user.job,
        id=user_id,
        created_at=current_user.created_at
    )
    created_users[user_id] = updated_user
    
    return updated_user

@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: str):
    """Delete user by ID"""
    if user_id not in created_users:
        raise HTTPException(status_code=404, detail="User not found")
    
    del created_users[user_id]
    return None

@app.get("/not-found")
async def not_found():
    """Endpoint that always returns 404"""
    raise HTTPException(status_code=404, detail="Resource not found")

@app.get("/server-error")
async def server_error():
    """Endpoint that always returns 500"""
    raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/unauthorized")
async def unauthorized():
    """Endpoint that always returns 401"""
    raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/forbidden")
async def forbidden():
    """Endpoint that always returns 403"""
    raise HTTPException(status_code=403, detail="Forbidden")

@app.get("/headers")
async def check_headers(request: Request):
    """Return request headers for testing"""
    return {
        "headers": dict(request.headers),
        "message": "Headers received successfully"
    }

@app.post("/echo")
async def echo(request: Request):
    """Echo back the request body"""
    body = await request.body()
    return {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
        "body": body.decode() if body else None
    }

if __name__ == "__main__":
    print("🚀 Starting Test API Server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔗 Base URL: http://localhost:8000")
    print("⏹️  Press Ctrl+C to stop")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 