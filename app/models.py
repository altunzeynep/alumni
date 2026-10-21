from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ==================== GRADUATE ====================
class Graduate(Base):
    __tablename__ = "graduates"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    graduation_year = Column(Integer)

class GraduateInput(BaseModel):
    full_name: str
    email: str
    graduation_year: int

class GraduatePartialUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    graduation_year: Optional[int] = None

class GraduateProfile(GraduateInput):
    id: int

    class Config:
        from_attributes = True


# ==================== ANNOUNCEMENT ====================
class Announcement(Base):
    __tablename__ = "announcements"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)

class AnnouncementInput(BaseModel):
    title: str
    content: str

class AnnouncementProfile(AnnouncementInput):
    id: int

    class Config:
        from_attributes = True


# ==================== JOB POSTING ====================
class JobPosting(Base):
    __tablename__ = "job_postings"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    company = Column(String(100), nullable=False)
    location = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # İsteğe bağlı: İlanı oluşturan mezun ile ilişki (Foreign Key)
    # graduate_id = Column(Integer, ForeignKey("graduates.id"), nullable=True)

class JobPostingInput(BaseModel):
    title: str
    description: str
    company: str
    location: Optional[str] = None

class JobPostingProfile(JobPostingInput):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


        # ==================== JOB APPLICATIONS ====================
class Application(Base):
    __tablename__ = "applications"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    job_posting_id = Column(Integer, ForeignKey("job_postings.id"), nullable=False)
    graduate_id = Column(Integer, ForeignKey("graduates.id"), nullable=False)
    status = Column(String(50), default="Pending", nullable=False)  # Pending, Accepted, Rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class ApplicationInput(BaseModel):
    job_posting_id: int
    graduate_id: int
    status: Optional[str] = "Pending"

class ApplicationProfile(ApplicationInput):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True