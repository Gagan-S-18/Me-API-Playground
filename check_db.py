#!/usr/bin/env python3
"""
Check database contents
"""

from database import SessionLocal, engine
import models

def check_database():
    print("🔍 Checking database...")
    
    # Create tables if they don't exist
    models.Base.metadata.create_all(bind=engine)
    print("✅ Database tables created/verified")
    
    # Check if we can connect
    try:
        db = SessionLocal()
        result = db.execute("SELECT 1").fetchone()
        print("✅ Database connection successful")
        db.close()
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return
    
    # Check profiles
    try:
        db = SessionLocal()
        profiles = db.query(models.Profile).all()
        print(f"📊 Found {len(profiles)} profiles in database")
        
        for profile in profiles:
            print(f"  - {profile.name} ({profile.email})")
        
        db.close()
    except Exception as e:
        print(f"❌ Error reading profiles: {e}")
    
    # Check skills
    try:
        db = SessionLocal()
        skills = db.query(models.Skill).all()
        print(f"🛠️ Found {len(skills)} skills in database")
        db.close()
    except Exception as e:
        print(f"❌ Error reading skills: {e}")
    
    # Check projects
    try:
        db = SessionLocal()
        projects = db.query(models.Project).all()
        print(f"🚀 Found {len(projects)} projects in database")
        db.close()
    except Exception as e:
        print(f"❌ Error reading projects: {e}")

if __name__ == "__main__":
    check_database()