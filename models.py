from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# Profile Management Models
class Profile(Base):
    __tablename__ = "profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    education = Column(Text)
    bio = Column(Text)
    location = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    skills = relationship("Skill", back_populates="profile", cascade="all, delete-orphan")
    projects = relationship("Project", back_populates="profile", cascade="all, delete-orphan")
    work_experiences = relationship("WorkExperience", back_populates="profile", cascade="all, delete-orphan")
    links = relationship("ProfileLink", back_populates="profile", cascade="all, delete-orphan")

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    name = Column(String(100), nullable=False)
    level = Column(String(20), default="intermediate")  # beginner, intermediate, advanced, expert
    category = Column(String(50))  # programming, framework, tool, language, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    profile = relationship("Profile", back_populates="skills")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    technologies = Column(JSON)  # Array of technologies used
    github_url = Column(String(500))
    live_url = Column(String(500))
    image_url = Column(String(500))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    profile = relationship("Profile", back_populates="projects")

class WorkExperience(Base):
    __tablename__ = "work_experiences"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    company = Column(String(200), nullable=False)
    position = Column(String(200), nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    is_current = Column(Boolean, default=False)
    location = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    profile = relationship("Profile", back_populates="work_experiences")

class ProfileLink(Base):
    __tablename__ = "profile_links"
    
    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    platform = Column(String(50), nullable=False)  # github, linkedin, portfolio, twitter, etc.
    url = Column(String(500), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    profile = relationship("Profile", back_populates="links")

# Legacy Wallet Management Models (keeping for backward compatibility)
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    wallet = relationship("Wallet", back_populates="user", uselist=False)
    transactions = relationship("Transaction", back_populates="user")

class Wallet(Base):
    __tablename__ = "wallets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    balance = Column(Float, default=0.0, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="wallet")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_type = Column(String(20), nullable=False)  # "credit" or "debit"
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="transactions")
