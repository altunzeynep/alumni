from sqlalchemy import Column, Integer, String
from app.database import Base
from pydantic import BaseModel
from typing import Optional

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


        # Duyurular için model
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