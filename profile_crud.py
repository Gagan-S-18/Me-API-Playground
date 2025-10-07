from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_, desc
from typing import List, Dict, Any, Optional
import models
import profile_schemas

# Profile CRUD Operations
def get_profile(db: Session, profile_id: int):
    """Get a profile by ID"""
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()

def get_profile_by_email(db: Session, email: str):
    """Get a profile by email"""
    return db.query(models.Profile).filter(models.Profile.email == email).first()

def create_profile(db: Session, profile: profile_schemas.ProfileCreate):
    """Create a new profile"""
    db_profile = models.Profile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def update_profile(db: Session, profile_id: int, profile_update: profile_schemas.ProfileUpdate):
    """Update a profile"""
    db_profile = get_profile(db, profile_id)
    if not db_profile:
        return None
    
    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_profile, field, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

def delete_profile(db: Session, profile_id: int):
    """Delete a profile and all related data"""
    db_profile = get_profile(db, profile_id)
    if not db_profile:
        return False
    
    db.delete(db_profile)
    db.commit()
    return True

def get_all_profiles(db: Session, skip: int = 0, limit: int = 100):
    """Get all profiles with pagination"""
    return db.query(models.Profile).offset(skip).limit(limit).all()

# Skill CRUD Operations
def create_skill(db: Session, profile_id: int, skill: profile_schemas.SkillCreate):
    """Add a skill to a profile"""
    db_skill = models.Skill(profile_id=profile_id, **skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

def get_skills_by_profile(db: Session, profile_id: int):
    """Get all skills for a profile"""
    return db.query(models.Skill).filter(models.Skill.profile_id == profile_id).all()

def update_skill(db: Session, skill_id: int, skill_update: profile_schemas.SkillUpdate):
    """Update a skill"""
    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not db_skill:
        return None
    
    update_data = skill_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_skill, field, value)
    
    db.commit()
    db.refresh(db_skill)
    return db_skill

def delete_skill(db: Session, skill_id: int):
    """Delete a skill"""
    db_skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not db_skill:
        return False
    
    db.delete(db_skill)
    db.commit()
    return True

def get_top_skills(db: Session, limit: int = 10):
    """Get most common skills across all profiles"""
    skill_counts = db.query(
        models.Skill.name,
        func.count(models.Skill.id).label('count')
    ).group_by(models.Skill.name).order_by(desc('count')).limit(limit).all()
    
    return [{"name": skill.name, "count": skill.count} for skill in skill_counts]

def search_skills(db: Session, skill_name: str, level: Optional[str] = None):
    """Search for skills by name and optionally by level"""
    query = db.query(models.Skill).filter(
        models.Skill.name.ilike(f"%{skill_name}%")
    )
    
    if level:
        query = query.filter(models.Skill.level == level)
    
    return query.all()

# Project CRUD Operations
def create_project(db: Session, profile_id: int, project: profile_schemas.ProjectCreate):
    """Add a project to a profile"""
    db_project = models.Project(profile_id=profile_id, **project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def get_projects_by_profile(db: Session, profile_id: int):
    """Get all projects for a profile"""
    return db.query(models.Project).filter(models.Project.profile_id == profile_id).all()

def get_projects_by_skill(db: Session, skill: str):
    """Get projects that use a specific skill/technology"""
    return db.query(models.Project).filter(
        models.Project.technologies.contains([skill])
    ).all()
    
def get_all_projects(db: Session, skip: int = 0, limit: int = 100):
    """Get all projects with pagination"""
    return db.query(models.Project).offset(skip).limit(limit).all()


def search_projects(db: Session, query: str, limit: int = 10):
    """Search projects by title, description, or technologies"""
    return db.query(models.Project).filter(
        or_(
            models.Project.title.ilike(f"%{query}%"),
            models.Project.description.ilike(f"%{query}%"),
            models.Project.technologies.contains([query])
        )
    ).limit(limit).all()

def update_project(db: Session, project_id: int, project_update: profile_schemas.ProjectUpdate):
    """Update a project"""
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        return None
    
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int):
    """Delete a project"""
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        return False
    
    db.delete(db_project)
    db.commit()
    return True

# Work Experience CRUD Operations
def create_work_experience(db: Session, profile_id: int, work_exp: profile_schemas.WorkExperienceCreate):
    """Add work experience to a profile"""
    db_work = models.WorkExperience(profile_id=profile_id, **work_exp.dict())
    db.add(db_work)
    db.commit()
    db.refresh(db_work)
    return db_work

def get_work_experiences_by_profile(db: Session, profile_id: int):
    """Get all work experiences for a profile"""
    return db.query(models.WorkExperience).filter(
        models.WorkExperience.profile_id == profile_id
    ).order_by(desc(models.WorkExperience.start_date)).all()

def update_work_experience(db: Session, work_id: int, work_update: profile_schemas.WorkExperienceUpdate):
    """Update work experience"""
    db_work = db.query(models.WorkExperience).filter(models.WorkExperience.id == work_id).first()
    if not db_work:
        return None
    
    update_data = work_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_work, field, value)
    
    db.commit()
    db.refresh(db_work)
    return db_work

def delete_work_experience(db: Session, work_id: int):
    """Delete work experience"""
    db_work = db.query(models.WorkExperience).filter(models.WorkExperience.id == work_id).first()
    if not db_work:
        return False
    
    db.delete(db_work)
    db.commit()
    return True

# Profile Link CRUD Operations
def create_profile_link(db: Session, profile_id: int, link: profile_schemas.ProfileLinkCreate):
    """Add a profile link"""
    db_link = models.ProfileLink(profile_id=profile_id, **link.dict())
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

def get_links_by_profile(db: Session, profile_id: int):
    """Get all links for a profile"""
    return db.query(models.ProfileLink).filter(models.ProfileLink.profile_id == profile_id).all()

def update_profile_link(db: Session, link_id: int, link_update: profile_schemas.ProfileLinkUpdate):
    """Update a profile link"""
    db_link = db.query(models.ProfileLink).filter(models.ProfileLink.id == link_id).first()
    if not db_link:
        return None
    
    update_data = link_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_link, field, value)
    
    db.commit()
    db.refresh(db_link)
    return db_link

def delete_profile_link(db: Session, link_id: int):
    """Delete a profile link"""
    db_link = db.query(models.ProfileLink).filter(models.ProfileLink.id == link_id).first()
    if not db_link:
        return False
    
    db.delete(db_link)
    db.commit()
    return True

# Search and Query Functions
def global_search(db: Session, query: str, limit: int = 10):
    """Global search across profiles, skills, projects, and work experiences"""
    results = []
    
    # Search profiles
    profiles = db.query(models.Profile).filter(
        or_(
            models.Profile.name.ilike(f"%{query}%"),
            models.Profile.bio.ilike(f"%{query}%"),
            models.Profile.education.ilike(f"%{query}%")
        )
    ).limit(limit).all()
    
    for profile in profiles:
        results.append({
            "type": "profile",
            "id": profile.id,
            "name": profile.name,
            "email": profile.email,
            "bio": profile.bio
        })
    
    # Search skills
    skills = db.query(models.Skill).filter(
        models.Skill.name.ilike(f"%{query}%")
    ).limit(limit).all()
    
    for skill in skills:
        results.append({
            "type": "skill",
            "id": skill.id,
            "name": skill.name,
            "level": skill.level,
            "profile_id": skill.profile_id
        })
    
    # Search projects
    projects = db.query(models.Project).filter(
        or_(
            models.Project.title.ilike(f"%{query}%"),
            models.Project.description.ilike(f"%{query}%")
        )
    ).limit(limit).all()
    
    for project in projects:
        results.append({
            "type": "project",
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "profile_id": project.profile_id
        })
    
    return results[:limit]

def get_complete_profile(db: Session, profile_id: int):
    """Get a complete profile with all related data"""
    profile = get_profile(db, profile_id)
    if not profile:
        return None

    return {
        "id": profile.id,
        "name": profile.name,
        "email": profile.email,
        "education": profile.education,
        "bio": profile.bio,
        "location": profile.location,
        "created_at": profile.created_at,
        "updated_at": profile.updated_at,
        "skills": get_skills_by_profile(db, profile_id),
        "projects": get_projects_by_profile(db, profile_id),
        "work_experiences": get_work_experiences_by_profile(db, profile_id),
        "links": get_links_by_profile(db, profile_id),
    }
