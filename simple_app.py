#!/usr/bin/env python3
"""
Simplified Me-API Playground for debugging
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from datetime import datetime

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Me-API Playground (Simple)",
    description="A simplified version for debugging",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Simple health check
@app.get("/health")
async def health_check():
    """Simple health check"""
    try:
        # Test database connection
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "connected"
    except Exception as e:
        print(f"Database error: {e}")
        db_status = "disconnected"
    
    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status,
        "timestamp": datetime.now(),
        "version": "1.0.0"
    }

# Simple root endpoint
@app.get("/")
async def root():
    """Simple root endpoint"""
    return {"message": "Me-API Playground is running!", "status": "ok"}

# Simple profiles endpoint
@app.get("/profiles")
async def get_profiles():
    """Get all profiles"""
    try:
        db = SessionLocal()
        profiles = db.query(models.Profile).all()
        db.close()
        
        result = []
        for profile in profiles:
            result.append({
                "id": profile.id,
                "name": profile.name,
                "email": profile.email,
                "education": profile.education,
                "bio": profile.bio,
                "location": profile.location
            })
        
        return result
    except Exception as e:
        print(f"Error getting profiles: {e}")
        return {"error": str(e), "profiles": []}

# Simple search endpoint
@app.get("/search")
async def search(q: str = "test"):
    """Simple search"""
    try:
        db = SessionLocal()
        profiles = db.query(models.Profile).filter(
            models.Profile.name.ilike(f"%{q}%")
        ).all()
        db.close()
        
        result = []
        for profile in profiles:
            result.append({
                "type": "profile",
                "id": profile.id,
                "name": profile.name,
                "email": profile.email
            })
        
        return {"results": result, "total": len(result), "query": q}
    except Exception as e:
        print(f"Error searching: {e}")
        return {"error": str(e), "results": [], "total": 0, "query": q}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)