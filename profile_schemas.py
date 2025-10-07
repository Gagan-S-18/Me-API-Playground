from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import re

# Profile Schemas
class ProfileBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Full name")
    email: EmailStr = Field(..., description="Email address")
    education: Optional[str] = Field(None, description="Educational background")
    bio: Optional[str] = Field(None, max_length=1000, description="Personal bio")
    location: Optional[str] = Field(None, max_length=100, description="Location")

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    education: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=1000)
    location: Optional[str] = Field(None, max_length=100)

class Profile(ProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Skill Schemas
class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Skill name")
    level: str = Field(default="intermediate", description="Skill level")
    category: Optional[str] = Field(None, max_length=50, description="Skill category")

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    level: Optional[str] = None
    category: Optional[str] = Field(None, max_length=50)

class Skill(SkillBase):
    id: int
    profile_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Project Schemas
class ProjectBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Project title")
    description: Optional[str] = Field(None, description="Project description")
    technologies: Optional[List[str]] = Field(default=[], description="Technologies used")
    github_url: Optional[str] = Field(None, max_length=500, description="GitHub repository URL")
    live_url: Optional[str] = Field(None, max_length=500, description="Live demo URL")
    image_url: Optional[str] = Field(None, max_length=500, description="Project image URL")
    start_date: Optional[datetime] = Field(None, description="Project start date")
    end_date: Optional[datetime] = Field(None, description="Project end date")
    is_active: bool = Field(default=True, description="Whether project is currently active")

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    technologies: Optional[List[str]] = None
    github_url: Optional[str] = Field(None, max_length=500)
    live_url: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = Field(None, max_length=500)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: Optional[bool] = None

class Project(ProjectBase):
    id: int
    profile_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Work Experience Schemas
class WorkExperienceBase(BaseModel):
    company: str = Field(..., min_length=1, max_length=200, description="Company name")
    position: str = Field(..., min_length=1, max_length=200, description="Job position")
    description: Optional[str] = Field(None, description="Job description")
    start_date: datetime = Field(..., description="Start date")
    end_date: Optional[datetime] = Field(None, description="End date")
    is_current: bool = Field(default=False, description="Whether currently working here")
    location: Optional[str] = Field(None, max_length=100, description="Work location")

class WorkExperienceCreate(WorkExperienceBase):
    pass

class WorkExperienceUpdate(BaseModel):
    company: Optional[str] = Field(None, min_length=1, max_length=200)
    position: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_current: Optional[bool] = None
    location: Optional[str] = Field(None, max_length=100)

class WorkExperience(WorkExperienceBase):
    id: int
    profile_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Profile Link Schemas
class ProfileLinkBase(BaseModel):
    platform: str = Field(..., min_length=1, max_length=50, description="Platform name")
    url: str = Field(..., max_length=500, description="Profile URL")
    
    @field_validator('url')
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        return v

class ProfileLinkCreate(ProfileLinkBase):
    pass

class ProfileLinkUpdate(BaseModel):
    platform: Optional[str] = Field(None, min_length=1, max_length=50)
    url: Optional[str] = Field(None, max_length=500)

class ProfileLink(ProfileLinkBase):
    id: int
    profile_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Complete Profile Response
class ProfileComplete(Profile):
    skills: List[Skill] = []
    projects: List[Project] = []
    work_experiences: List[WorkExperience] = []
    links: List[ProfileLink] = []

# Search and Query Schemas
class SearchQuery(BaseModel):
    q: str = Field(..., min_length=1, description="Search query")
    limit: int = Field(default=10, ge=1, le=100, description="Maximum number of results")

class SkillQuery(BaseModel):
    skill: str = Field(..., min_length=1, description="Skill to search for")
    level: Optional[str] = Field(None, description="Filter by skill level")

class TopSkillsResponse(BaseModel):
    skills: List[Dict[str, Any]]
    total: int

class ProjectSearchResponse(BaseModel):
    projects: List[Project]
    total: int

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]
    total: int
    query: str

# Health Check Schema
class HealthCheck(BaseModel):
    status: str
    database: str
    timestamp: datetime
    version: str = "1.0.0"