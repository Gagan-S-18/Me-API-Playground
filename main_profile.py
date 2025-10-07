from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import models
import profile_schemas
import profile_crud
from database import SessionLocal, engine
from datetime import datetime
import logging 
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Me-API Playground",
    description="A comprehensive profile management API playground for showcasing skills, projects, and experience",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for frontend (only if directory exists)
import os
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health Check Endpoint
@app.get("/health", response_model=profile_schemas.HealthCheck, tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint for liveness checks.
    
    Returns:
        Health status of the API and database
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        db_status = "disconnected"
    
    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "database": db_status,
        "timestamp": datetime.now(),
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/", response_class=HTMLResponse, tags=["Frontend"])
async def root():
    """
    Serve the main frontend page.
    """
    try:
        with open("static/index.html", "r",encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <html>
            <head><title>Me-API Playground</title></head>
            <body>
                <h1>Me-API Playground</h1>
                <p>Welcome to the Me-API Playground! Check out the <a href="/docs">API documentation</a>.</p>
            </body>
        </html>
        """)

# Profile Management Endpoints
@app.post("/profiles", response_model=profile_schemas.Profile, tags=["Profiles"])
async def create_profile(profile: profile_schemas.ProfileCreate, db: Session = Depends(get_db)):
    """
    Create a new profile.
    
    Args:
        profile: Profile creation details
        
    Returns:
        Created profile information
    """
    # Check if email already exists
    existing_profile = profile_crud.get_profile_by_email(db, profile.email)
    if existing_profile:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    return profile_crud.create_profile(db, profile)

@app.get("/profiles", response_model=List[profile_schemas.Profile], tags=["Profiles"])
async def list_profiles(
    skip: int = Query(0, ge=0, description="Number of profiles to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of profiles to return"),
    db: Session = Depends(get_db)
):
    """
    List all profiles with pagination.
    
    Args:
        skip: Number of profiles to skip
        limit: Maximum number of profiles to return
        
    Returns:
        List of profiles
    """
    return profile_crud.get_all_profiles(db, skip=skip, limit=limit)

@app.get("/profiles/{profile_id}", response_model=profile_schemas.ProfileComplete, tags=["Profiles"])
async def get_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Get a complete profile with all related data.
    
    Args:
        profile_id: ID of the profile to retrieve
        
    Returns:
        Complete profile information including skills, projects, work experience, and links
    """
    profile = profile_crud.get_complete_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.put("/profiles/{profile_id}", response_model=profile_schemas.Profile, tags=["Profiles"])
async def update_profile(
    profile_id: int, 
    profile_update: profile_schemas.ProfileUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update a profile.
    
    Args:
        profile_id: ID of the profile to update
        profile_update: Profile update details
        
    Returns:
        Updated profile information
    """
    profile = profile_crud.update_profile(db, profile_id, profile_update)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@app.delete("/profiles/{profile_id}", tags=["Profiles"])
async def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    """
    Delete a profile and all related data.
    
    Args:
        profile_id: ID of the profile to delete
        
    Returns:
        Success message
    """
    success = profile_crud.delete_profile(db, profile_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"message": "Profile deleted successfully"}

# Skills Management Endpoints
@app.post("/profiles/{profile_id}/skills", response_model=profile_schemas.Skill, tags=["Skills"])
async def add_skill(
    profile_id: int, 
    skill: profile_schemas.SkillCreate, 
    db: Session = Depends(get_db)
):
    """
    Add a skill to a profile.
    
    Args:
        profile_id: ID of the profile
        skill: Skill details
        
    Returns:
        Created skill information
    """
    # Check if profile exists
    profile = profile_crud.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile_crud.create_skill(db, profile_id, skill)

@app.get("/profiles/{profile_id}/skills", response_model=List[profile_schemas.Skill], tags=["Skills"])
async def get_profile_skills(profile_id: int, db: Session = Depends(get_db)):
    """
    Get all skills for a profile.
    
    Args:
        profile_id: ID of the profile
        
    Returns:
        List of skills for the profile
    """
    # Check if profile exists
    profile = profile_crud.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile_crud.get_skills_by_profile(db, profile_id)

@app.get("/skills/top", response_model=profile_schemas.TopSkillsResponse, tags=["Skills"])
async def get_top_skills(
    limit: int = Query(10, ge=1, le=100, description="Number of top skills to return"),
    db: Session = Depends(get_db)
):
    """
    Get the most common skills across all profiles.
    
    Args:
        limit: Number of top skills to return
        
    Returns:
        List of most common skills with their counts
    """
    skills = profile_crud.get_top_skills(db, limit)
    return {"skills": skills, "total": len(skills)}

# Projects Management Endpoints
@app.post("/profiles/{profile_id}/projects", response_model=profile_schemas.Project, tags=["Projects"])
async def add_project(
    profile_id: int, 
    project: profile_schemas.ProjectCreate, 
    db: Session = Depends(get_db)
):
    """
    Add a project to a profile.
    
    Args:
        profile_id: ID of the profile
        project: Project details
        
    Returns:
        Created project information
    """
    # Check if profile exists
    profile = profile_crud.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile_crud.create_project(db, profile_id, project)

@app.get("/profiles/{profile_id}/projects", response_model=List[profile_schemas.Project], tags=["Projects"])
async def get_profile_projects(profile_id: int, db: Session = Depends(get_db)):
    """
    Get all projects for a profile.
    
    Args:
        profile_id: ID of the profile
        
    Returns:
        List of projects for the profile
    """
    # Check if profile exists
    profile = profile_crud.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile_crud.get_projects_by_profile(db, profile_id)

@app.get("/projects", response_model=profile_schemas.ProjectSearchResponse, tags=["Projects"])
async def search_projects_by_skill(
    skill: str = Query(..., description="Skill/technology to search for"),
    db: Session = Depends(get_db)
):
    """
    Get projects that use a specific skill/technology.
    
    Args:
        skill: Skill/technology to search for
        
    Returns:
        List of projects using the specified skill
    """
    projects = profile_crud.get_projects_by_skill(db, skill)
    return {"projects": projects, "total": len(projects)}

@app.get("/projects/all", response_model=List[profile_schemas.Project], tags=["Projects"])
async def list_all_projects(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of projects to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of projects to return")
):
    """
    List all projects with pagination.
    
    Args:
        skip: Number of projects to skip
        limit: Maximum number of projects to return
        
    Returns:
        List of projects
    """
    return profile_crud.get_all_projects(db, skip=skip, limit=limit)


# Work Experience Management Endpoints
@app.post("/profiles/{profile_id}/work", response_model=profile_schemas.WorkExperience, tags=["Work Experience"])
async def add_work_experience(
    profile_id: int, 
    work_exp: profile_schemas.WorkExperienceCreate, 
    db: Session = Depends(get_db)
):
    """
    Add work experience to a profile.
    
    Args:
        profile_id: ID of the profile
        work_exp: Work experience details
        
    Returns:
        Created work experience information
    """
    # Check if profile exists
    profile = profile_crud.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile_crud.create_work_experience(db, profile_id, work_exp)

@app.get("/profiles/{profile_id}/work", response_model=List[profile_schemas.WorkExperience], tags=["Work Experience"])
async def get_profile_work_experience(profile_id: int, db: Session = Depends(get_db)):
    """
    Get all work experiences for a profile.
    
    Args:
        profile_id: ID of the profile
        
    Returns:
        List of work experiences for the profile
    """
    # Check if profile exists
    profile = profile_crud.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile_crud.get_work_experiences_by_profile(db, profile_id)

# Profile Links Management Endpoints
@app.post("/profiles/{profile_id}/links", response_model=profile_schemas.ProfileLink, tags=["Profile Links"])
async def add_profile_link(
    profile_id: int, 
    link: profile_schemas.ProfileLinkCreate, 
    db: Session = Depends(get_db)
):
    """
    Add a profile link.
    
    Args:
        profile_id: ID of the profile
        link: Link details
        
    Returns:
        Created link information
    """
    # Check if profile exists
    profile = profile_crud.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile_crud.create_profile_link(db, profile_id, link)

@app.get("/profiles/{profile_id}/links", response_model=List[profile_schemas.ProfileLink], tags=["Profile Links"])
async def get_profile_links(profile_id: int, db: Session = Depends(get_db)):
    """
    Get all links for a profile.
    
    Args:
        profile_id: ID of the profile
        
    Returns:
        List of links for the profile
    """
    # Check if profile exists
    profile = profile_crud.get_profile(db, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return profile_crud.get_links_by_profile(db, profile_id)

# Search Endpoints
@app.get("/search", response_model=profile_schemas.SearchResponse, tags=["Search"])
async def global_search(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Global search across profiles, skills, projects, and work experiences.
    
    Args:
        q: Search query
        limit: Maximum number of results to return
        
    Returns:
        Search results across all content types
    """
    results = profile_crud.global_search(db, q, limit)
    return {"results": results, "total": len(results), "query": q}

# Skills Search Endpoint
@app.get("/skills/search", response_model=List[profile_schemas.Skill], tags=["Skills"])
async def search_skills(
    skill: str = Query(..., min_length=1, description="Skill name to search for"),
    level: Optional[str] = Query(None, description="Filter by skill level"),
    db: Session = Depends(get_db)
):
    """
    Search for skills by name and optionally by level.
    
    Args:
        skill: Skill name to search for
        level: Optional skill level filter
        
    Returns:
        List of matching skills
    """
    return profile_crud.search_skills(db, skill, level)

@app.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    profiles_count = db.query(models.Profile).count()
    skills_count = db.query(models.Skill).count()
    projects_count = db.query(models.Project).count()

    return {
        "profiles": profiles_count,
        "skills": skills_count,
        "projects": projects_count
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
