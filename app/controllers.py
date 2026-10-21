from fastapi import APIRouter, HTTPException, status, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import (
    Graduate, 
    Announcement, 
    JobPosting,
    GraduateInput, 
    GraduatePartialUpdate, 
    GraduateProfile, 
    AnnouncementInput, 
    AnnouncementProfile,
    JobPostingInput,
    JobPostingProfile
)

router = APIRouter()

# HTML Şablon Motoru Tanımı
templates = Jinja2Templates(directory="templates")

# --- Hafta 2: Temel Rotalar ---
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


# --- Hafta 3 & 4: Gerçek Veritabanı Üzerinden Mezunlar (Graduates) CRUD Operasyonları ---
@router.get("/api/users", response_model=List[GraduateProfile], tags=["User Management"])
def list_graduates(db: Session = Depends(get_db)):
    return db.query(Graduate).all()

@router.get("/api/users/{user_id}", response_model=GraduateProfile, tags=["User Management"])
def fetch_graduate(user_id: int, db: Session = Depends(get_db)):
    match = db.query(Graduate).filter(Graduate.id == user_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Graduate record not found.")
    return match

@router.post("/api/users", status_code=status.HTTP_201_CREATED, tags=["User Management"])
def register_graduate(payload: GraduateInput, db: Session = Depends(get_db)):
    new_record = Graduate(full_name=payload.full_name, contact_email=payload.contact_email)
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return {"message": "Successfully registered via DB Controller", "data": new_record}

@router.put("/api/users/{user_id}", tags=["User Management"])
def overwrite_graduate(user_id: int, payload: GraduateInput, db: Session = Depends(get_db)):
    match = db.query(Graduate).filter(Graduate.id == user_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Graduate record not found.")
    match.full_name = payload.full_name
    match.contact_email = payload.contact_email
    db.commit()
    db.refresh(match)
    return {"message": "Record fully updated (PUT)", "data": match}

@router.patch("/api/users/{user_id}", tags=["User Management"])
def modify_graduate(user_id: int, payload: GraduatePartialUpdate, db: Session = Depends(get_db)):
    match = db.query(Graduate).filter(Graduate.id == user_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Graduate record not found.")
    if payload.full_name is not None:
        match.full_name = payload.full_name
    if payload.contact_email is not None:
        match.contact_email = payload.contact_email
    db.commit()
    db.refresh(match)
    return {"message": "Record partially modified (PATCH)", "data": match}

@router.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["User Management"])
def purge_graduate(user_id: int, db: Session = Depends(get_db)):
    match = db.query(Graduate).filter(Graduate.id == user_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Graduate record not found.")
    db.delete(match)
    db.commit()
    return None


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
@router.get("/api/announcements", response_model=List[AnnouncementProfile], tags=["Announcements"])
def list_announcements(db: Session = Depends(get_db)):
    return db.query(Announcement).all()

@router.post("/api/announcements", status_code=201, tags=["Announcements"])
def create_announcement(payload: AnnouncementInput, db: Session = Depends(get_db)):
    new_announcement = Announcement(title=payload.title, content=payload.content)
    db.add(new_announcement)
    db.commit()
    db.refresh(new_announcement)
    return {"message": "Announcement created successfully", "data": new_announcement}


# --- JOB POSTINGS API (İş İlanları Operasyonları) ---
@router.get("/api/job-postings", response_model=List[JobPostingProfile], tags=["Job Postings"])
def list_job_postings(db: Session = Depends(get_db)):
    return db.query(JobPosting).all()

@router.get("/api/job-postings/{job_id}", response_model=JobPostingProfile, tags=["Job Postings"])
def fetch_job_posting(job_id: int, db: Session = Depends(get_db)):
    match = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Job posting record not found.")
    return match

@router.post("/api/job-postings", status_code=status.HTTP_201_CREATED, tags=["Job Postings"])
def create_job_posting(payload: JobPostingInput, db: Session = Depends(get_db)):
    new_job = JobPosting(
        title=payload.title,
        description=payload.description,
        company=payload.company,
        location=payload.location
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return {"message": "Job posting created successfully", "data": new_job}

@router.delete("/api/job-postings/{job_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Job Postings"])
def delete_job_posting(job_id: int, db: Session = Depends(get_db)):
    match = db.query(JobPosting).filter(JobPosting.id == job_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Job posting record not found.")
    db.delete(match)
    db.commit()
    return None

# --- APPLICATIONS API (İş Başvuruları Operasyonları) ---
@router.get("/api/applications", response_model=List[ApplicationProfile], tags=["Applications"])
def list_applications(db: Session = Depends(get_db)):
    return db.query(Application).all()

@router.get("/api/applications/{app_id}", response_model=ApplicationProfile, tags=["Applications"])
def fetch_application(app_id: int, db: Session = Depends(get_db)):
    match = db.query(Application).filter(Application.id == app_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Application record not found.")
    return match

@router.post("/api/applications", status_code=status.HTTP_201_CREATED, tags=["Applications"])
def create_application(payload: ApplicationInput, db: Session = Depends(get_db)):
    new_app = Application(
        job_posting_id=payload.job_posting_id,
        graduate_id=payload.graduate_id,
        status=payload.status
    )
    db.add(new_app)
    db.commit()
    db.refresh(new_app)
    return {"message": "Application submitted successfully", "data": new_app}

@router.delete("/api/applications/{app_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Applications"])
def delete_application(app_id: int, db: Session = Depends(get_db)):
    match = db.query(Application).filter(Application.id == app_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Application record not found.")
    db.delete(match)
    db.commit()
    return None


# --- SEED DATA (Test Verileri Ekleme) ---
@router.post("/api/seed/job-postings", status_code=status.HTTP_201_CREATED, tags=["Job Postings"])
def seed_job_postings(db: Session = Depends(get_db)):
    # Eğer tabloda zaten veri varsa tekrar doldurmasın
    existing_count = db.query(JobPosting).count()
    if existing_count > 0:
        return {"message": f"Table already has {existing_count} job postings. No seed needed."}

    sample_jobs = [
        JobPosting(
            title="Junior Python Developer",
            description="En az 1 yıl FastAPI/Django deneyimli, OOP ve PostgreSQL bilen takım arkadaşı arıyoruz.",
            company="Tech Innovators A.Ş.",
            location="İstanbul (Hibrit)"
        ),
        JobPosting(
            title="Frontend Web Developer",
            description="JavaScript, HTML, CSS ve modern framework'lere hakim mezunlar aranıyor.",
            company="Digital Studio",
            location="Uzaktan (Remote)"
        ),
        JobPosting(
            title="Data Analyst",
            description="SQL, Python (Pandas/NumPy) ve veri görselleştirme araçlarında yetkin çalışma arkadaşı.",
            company="DataCorp Global",
            location="Ankara"
        )
    ]

    db.add_all(sample_jobs)
    db.commit()
    return {"message": "Job postings table successfully seeded with sample data!", "count": len(sample_jobs)}


# --- NESTED ROUTE: Belirli Bir İlana Ait Başvurular ---
@router.get("/api/job-postings/{job_id}/applications", response_model=List[ApplicationProfile], tags=["Job Postings", "Applications"])
def list_job_applications(job_id: int, db: Session = Depends(get_db)):
    applications = db.query(Application).filter(Application.job_posting_id == job_id).all()
    return applications