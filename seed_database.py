"""
Database seeding script for Me-API Playground
This script populates the database with sample profile data
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import profile_crud
import profile_schemas
from datetime import datetime, timedelta
import random

def create_sample_profile_data():
    """Create comprehensive sample profile data"""
    
    # Sample profile data
    sample_profiles = [
        {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "education": "Bachelor's in Computer Science from MIT",
            "bio": "Full-stack developer with 5+ years of experience in web development. Passionate about creating scalable applications and learning new technologies.",
            "location": "San Francisco, CA",
            "skills": [
                {"name": "Python", "level": "expert", "category": "programming"},
                {"name": "JavaScript", "level": "advanced", "category": "programming"},
                {"name": "React", "level": "advanced", "category": "framework"},
                {"name": "Node.js", "level": "advanced", "category": "framework"},
                {"name": "PostgreSQL", "level": "intermediate", "category": "database"},
                {"name": "Docker", "level": "intermediate", "category": "tool"},
                {"name": "AWS", "level": "intermediate", "category": "cloud"},
                {"name": "Git", "level": "advanced", "category": "tool"}
            ],
            "projects": [
                {
                    "title": "E-Commerce Platform",
                    "description": "A full-stack e-commerce platform built with React, Node.js, and PostgreSQL. Features include user authentication, payment processing, and inventory management.",
                    "technologies": ["React", "Node.js", "PostgreSQL", "Stripe", "Docker"],
                    "github_url": "https://github.com/johndoe/ecommerce-platform",
                    "live_url": "https://ecommerce-demo.com",
                    "start_date": datetime.now() - timedelta(days=180),
                    "end_date": datetime.now() - timedelta(days=30),
                    "is_active": False
                },
                {
                    "title": "Task Management App",
                    "description": "A collaborative task management application with real-time updates using WebSockets.",
                    "technologies": ["React", "Socket.io", "Express", "MongoDB"],
                    "github_url": "https://github.com/johndoe/task-manager",
                    "live_url": "https://taskmanager-demo.com",
                    "start_date": datetime.now() - timedelta(days=90),
                    "is_active": True
                },
                {
                    "title": "Machine Learning API",
                    "description": "RESTful API for machine learning model inference using FastAPI and scikit-learn.",
                    "technologies": ["Python", "FastAPI", "scikit-learn", "Docker", "Redis"],
                    "github_url": "https://github.com/johndoe/ml-api",
                    "live_url": "https://ml-api-demo.com",
                    "start_date": datetime.now() - timedelta(days=60),
                    "is_active": True
                }
            ],
            "work_experiences": [
                {
                    "company": "TechCorp Inc.",
                    "position": "Senior Software Engineer",
                    "description": "Led development of microservices architecture and mentored junior developers. Improved system performance by 40%.",
                    "start_date": datetime.now() - timedelta(days=730),
                    "is_current": True,
                    "location": "San Francisco, CA"
                },
                {
                    "company": "StartupXYZ",
                    "position": "Full-Stack Developer",
                    "description": "Developed and maintained web applications using React and Node.js. Collaborated with cross-functional teams.",
                    "start_date": datetime.now() - timedelta(days=1095),
                    "end_date": datetime.now() - timedelta(days=730),
                    "is_current": False,
                    "location": "New York, NY"
                }
            ],
            "links": [
                {"platform": "github", "url": "https://github.com/johndoe"},
                {"platform": "linkedin", "url": "https://linkedin.com/in/johndoe"},
                {"platform": "portfolio", "url": "https://johndoe.dev"}
            ]
        },
        {
            "name": "Jane Smith",
            "email": "jane.smith@example.com",
            "education": "Master's in Data Science from Stanford University",
            "bio": "Data scientist and machine learning engineer with expertise in Python, R, and cloud platforms. Passionate about using data to solve real-world problems.",
            "location": "Seattle, WA",
            "skills": [
                {"name": "Python", "level": "expert", "category": "programming"},
                {"name": "R", "level": "advanced", "category": "programming"},
                {"name": "TensorFlow", "level": "advanced", "category": "framework"},
                {"name": "PyTorch", "level": "intermediate", "category": "framework"},
                {"name": "Pandas", "level": "expert", "category": "library"},
                {"name": "Scikit-learn", "level": "advanced", "category": "library"},
                {"name": "AWS", "level": "advanced", "category": "cloud"},
                {"name": "SQL", "level": "expert", "category": "database"},
                {"name": "Jupyter", "level": "advanced", "category": "tool"}
            ],
            "projects": [
                {
                    "title": "Predictive Analytics Dashboard",
                    "description": "Real-time dashboard for predictive analytics using machine learning models and interactive visualizations.",
                    "technologies": ["Python", "Flask", "D3.js", "PostgreSQL", "Redis"],
                    "github_url": "https://github.com/janesmith/analytics-dashboard",
                    "live_url": "https://analytics-demo.com",
                    "start_date": datetime.now() - timedelta(days=120),
                    "is_active": True
                },
                {
                    "title": "NLP Text Classification",
                    "description": "Natural language processing model for text classification using transformer architectures.",
                    "technologies": ["Python", "TensorFlow", "Hugging Face", "Docker"],
                    "github_url": "https://github.com/janesmith/nlp-classifier",
                    "start_date": datetime.now() - timedelta(days=200),
                    "end_date": datetime.now() - timedelta(days=60),
                    "is_active": False
                }
            ],
            "work_experiences": [
                {
                    "company": "DataTech Solutions",
                    "position": "Senior Data Scientist",
                    "description": "Developed machine learning models for business intelligence and led data science initiatives.",
                    "start_date": datetime.now() - timedelta(days=365),
                    "is_current": True,
                    "location": "Seattle, WA"
                },
                {
                    "company": "Analytics Pro",
                    "position": "Data Scientist",
                    "description": "Built predictive models and statistical analyses for various business use cases.",
                    "start_date": datetime.now() - timedelta(days=730),
                    "end_date": datetime.now() - timedelta(days=365),
                    "is_current": False,
                    "location": "Austin, TX"
                }
            ],
            "links": [
                {"platform": "github", "url": "https://github.com/janesmith"},
                {"platform": "linkedin", "url": "https://linkedin.com/in/janesmith"},
                {"platform": "portfolio", "url": "https://janesmith.dev"},
                {"platform": "twitter", "url": "https://twitter.com/janesmith"}
            ]
        },
        {
            "name": "Mike Johnson",
            "email": "mike.johnson@example.com",
            "education": "Bachelor's in Software Engineering from UC Berkeley",
            "bio": "Mobile app developer specializing in iOS and Android development. Experienced in both native and cross-platform solutions.",
            "location": "Los Angeles, CA",
            "skills": [
                {"name": "Swift", "level": "expert", "category": "programming"},
                {"name": "Kotlin", "level": "advanced", "category": "programming"},
                {"name": "React Native", "level": "advanced", "category": "framework"},
                {"name": "Flutter", "level": "intermediate", "category": "framework"},
                {"name": "iOS", "level": "expert", "category": "platform"},
                {"name": "Android", "level": "advanced", "category": "platform"},
                {"name": "Firebase", "level": "advanced", "category": "cloud"},
                {"name": "Xcode", "level": "expert", "category": "tool"},
                {"name": "Android Studio", "level": "advanced", "category": "tool"}
            ],
            "projects": [
                {
                    "title": "Fitness Tracking App",
                    "description": "Cross-platform fitness tracking app with real-time workout monitoring and social features.",
                    "technologies": ["React Native", "Firebase", "Redux", "Expo"],
                    "github_url": "https://github.com/mikejohnson/fitness-app",
                    "live_url": "https://fitness-app-demo.com",
                    "start_date": datetime.now() - timedelta(days=150),
                    "is_active": True
                },
                {
                    "title": "Food Delivery iOS App",
                    "description": "Native iOS app for food delivery with real-time tracking and payment integration.",
                    "technologies": ["Swift", "UIKit", "Core Data", "Stripe"],
                    "github_url": "https://github.com/mikejohnson/food-delivery-ios",
                    "start_date": datetime.now() - timedelta(days=300),
                    "end_date": datetime.now() - timedelta(days=90),
                    "is_active": False
                }
            ],
            "work_experiences": [
                {
                    "company": "MobileFirst Inc.",
                    "position": "Senior Mobile Developer",
                    "description": "Lead mobile development for iOS and Android applications. Mentored junior developers and established coding standards.",
                    "start_date": datetime.now() - timedelta(days=500),
                    "is_current": True,
                    "location": "Los Angeles, CA"
                },
                {
                    "company": "AppStudio",
                    "position": "iOS Developer",
                    "description": "Developed native iOS applications using Swift and Objective-C. Collaborated with design and backend teams.",
                    "start_date": datetime.now() - timedelta(days=800),
                    "end_date": datetime.now() - timedelta(days=500),
                    "is_current": False,
                    "location": "San Diego, CA"
                }
            ],
            "links": [
                {"platform": "github", "url": "https://github.com/mikejohnson"},
                {"platform": "linkedin", "url": "https://linkedin.com/in/mikejohnson"},
                {"platform": "portfolio", "url": "https://mikejohnson.dev"}
            ]
        }
    ]
    
    return sample_profiles

def seed_database():
    """Seed the database with sample data"""
    db = SessionLocal()
    
    try:
        # Clear existing data
        print("Clearing existing data...")
        db.query(models.ProfileLink).delete()
        db.query(models.WorkExperience).delete()
        db.query(models.Project).delete()
        db.query(models.Skill).delete()
        db.query(models.Profile).delete()
        db.commit()
        
        # Get sample data
        sample_data = create_sample_profile_data()
        
        print(f"Creating {len(sample_data)} sample profiles...")
        
        for profile_data in sample_data:
            # Create profile
            profile_create = profile_schemas.ProfileCreate(
                name=profile_data["name"],
                email=profile_data["email"],
                education=profile_data["education"],
                bio=profile_data["bio"],
                location=profile_data["location"]
            )
            
            profile = profile_crud.create_profile(db, profile_create)
            print(f"Created profile: {profile.name}")
            
            # Add skills
            for skill_data in profile_data["skills"]:
                skill_create = profile_schemas.SkillCreate(**skill_data)
                profile_crud.create_skill(db, profile.id, skill_create)
            
            # Add projects
            for project_data in profile_data["projects"]:
                project_create = profile_schemas.ProjectCreate(**project_data)
                profile_crud.create_project(db, profile.id, project_create)
            
            # Add work experiences
            for work_data in profile_data["work_experiences"]:
                work_create = profile_schemas.WorkExperienceCreate(**work_data)
                profile_crud.create_work_experience(db, profile.id, work_create)
            
            # Add links
            for link_data in profile_data["links"]:
                link_create = profile_schemas.ProfileLinkCreate(**link_data)
                profile_crud.create_profile_link(db, profile.id, link_create)
        
        print("Database seeded successfully!")
        print(f"Created {len(sample_data)} profiles with associated data")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()