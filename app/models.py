from pydantic import BaseModel, EmailStr
from typing import Optional

class GraduateProfile(BaseModel):
    full_name: str
    contact_email: EmailStr

class GraduateInput(GraduateProfile):
    pass

class GraduatePartialUpdate(BaseModel):
    full_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None