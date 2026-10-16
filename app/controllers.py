from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models import GraduateInput, GraduatePartialUpdate, GraduateProfile


router = APIRouter()

# Hafta 2: Temel Rotalar
@router.get("/", tags=["System Status"])
def health_check():
    return {"status": "Online", "architecture": "MVC Pattern Active", "system": "Alumni Tracking System"}

@router.get("/hello", tags=["System Status"])
def index_greet():
    return "Greetings from Alumni MVC Service!"

@router.get("/hello/{name}", tags=["System Status"])
def personalized_greet(name: str):
    return f"Welcome aboard to MVC architecture, {name}!"

@router.get("/sum/{a}/{b}", tags=["Calculations"])
def compute_sum(a: int, b: int):
    return {"operand_1": a, "operand_2": b, "total": a + b}

@router.get("/about", tags=["System Status"])
def project_manifesto():
    return {"module": "Web Programming", "pattern": "MVC", "author": "Zeynep Altun"}

# Hafta 3 & 4: /api/users CRUD Operasyonları (MVC Controller Yapısıyla)
@router.get("/api/users", response_model=List[GraduateProfile], tags=["User Management"])
def list_graduates():
    return graduates_registry

@router.get("/api/users/{user_id}", response_model=GraduateProfile, tags=["User Management"])
def fetch_graduate(user_id: int):
    match = next((item for item in graduates_registry if item["id"] == user_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Graduate record not found.")
    return match

@router.post("/api/users", status_code=status.HTTP_201_CREATED, tags=["User Management"])
def register_graduate(payload: GraduateInput):
    new_id = max([item["id"] for item in graduates_registry], default=100) + 1
    record = {"id": new_id, "full_name": payload.full_name, "contact_email": payload.contact_email}
    graduates_registry.append(record)
    return {"id": new_id, "message": "Successfully registered via MVC Controller", "data": record}

@router.put("/api/users/{user_id}", tags=["User Management"])
def overwrite_graduate(user_id: int, payload: GraduateInput):
    match = next((item for item in graduates_registry if item["id"] == user_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Graduate record not found.")
    match["full_name"] = payload.full_name
    match["contact_email"] = payload.contact_email
    return {"message": "Record fully updated (PUT)", "data": match}

@router.patch("/api/users/{user_id}", tags=["User Management"])
def modify_graduate(user_id: int, payload: GraduatePartialUpdate):
    match = next((item for item in graduates_registry if item["id"] == user_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Graduate record not found.")
    if payload.full_name is not None:
        match["full_name"] = payload.full_name
    if payload.contact_email is not None:
        match["contact_email"] = payload.contact_email
    return {"message": "Record partially modified (PATCH)", "data": match}

@router.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["User Management"])
def purge_graduate(user_id: int):
    match = next((item for item in graduates_registry if item["id"] == user_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Graduate record not found.")
    graduates_registry.remove(match)
    return None


from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Graduate, Announcement, GraduateInput, AnnouncementInput

# HTML şablonları için klasör tanımı (proje kök dizininde templates/ klasörü olmalı)
templates = Jinja2Templates(directory="templates")

# --- WEB VIEWS (HTML Arayüzleri) ---
@router.get("/web/graduates", response_class=HTMLResponse, tags=["Web Views"])
def web_list_graduates(request: Request, db: Session = Depends(get_db)):
    graduates = db.query(Graduate).all()
    return templates.TemplateResponse("graduates.html", {"request": request, "graduates": graduates})

@router.get("/web/announcements", response_class=HTMLResponse, tags=["Web Views"])
def web_list_announcements(request: Request, db: Session = Depends(get_db)):
    announcements = db.query(Announcement).all()
    return templates.TemplateResponse("announcements.html", {"request": request, "announcements": announcements})


# --- ANNOUNCEMENTS API (Duyurular Ödevi) ---
@app_router.get("/api/announcements", response_class=List[AnnouncementProfile], tags=["Announcements"]) # Eğer router kullanıyorsan `@router` olarak ayarla
def list_announcements(db: Session = Depends(get_db)):
    return db.query(Announcement).all()

@router.post("/api/announcements", status_code=201, tags=["Announcements"])
def create_announcement(payload: AnnouncementInput, db: Session = Depends(get_db)):
    new_announcement = Announcement(title=payload.title, content=payload.content)
    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)
    return {"message": "Announcement created successfully", "data": new_announcement}