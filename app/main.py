from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional

app = FastAPI(
    title="Zeynep Altun - Alumni Tracking Core API",
    version="2.1.0",
    docs_url="/api/swagger",
    redoc_url=None
)

# Özgün Şema Yapıları
class GraduateProfile(BaseModel):
    full_name: str
    contact_email: EmailStr

class GraduateInput(GraduateProfile):
    pass

class GraduatePartialUpdate(BaseModel):
    full_name: Optional[str] = None
    contact_email: Optional[EmailStr] = None

# Benzersiz Veri Kaynağı Simülasyonu
graduates_registry = [
    {"id": 101, "full_name": "Zeynep Altun", "contact_email": "zeynep.altun@std.edu.tr"},
    {"id": 102, "full_name": "Mehmet Demir", "contact_email": "mehmet.demir@example.com"}
]

# Hafta 2: Temel Rotalar
@app.get("/", tags=["System Status"])
def health_check():
    return {"status": "Online", "system": "Alumni Tracking System API"}

@app.get("/hello", tags=["System Status"])
def index_greet():
    return "Greetings from Alumni Service!"

@app.get("/hello/{name}", tags=["System Status"])
def personalized_greet(name: str):
    return f"Welcome aboard, {name}!"

@app.get("/sum/{a}/{b}", tags=["Calculations"])
def compute_sum(a: int, b: int):
    return {"operand_1": a, "operand_2": b, "total": a + b}

@app.get("/about", tags=["System Status"])
def project_manifesto():
    return {"module": "Web Programming", "author": "Zeynep Altun", "scope": "Alumni Tracking"}

# Hafta 3: /api/users CRUD Operasyonları (PUT, PATCH, Swagger dahil)
@app.get("/api/users", response_model=List[GraduateProfile], tags=["User Management"])
def list_graduates():
    # Model uyumluluğu için anahtarları eşleştiriyoruz
    return [{"id": g["id"], "full_name": g["full_name"], "contact_email": g["contact_email"]} for g in graduates_registry]

@app.get("/api/users/{user_id}", response_model=GraduateProfile, tags=["User Management"])
def fetch_graduate(user_id: int):
    match = next((item for item in graduates_registry if item["id"] == user_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Graduate record not found.")
    return match

@app.post("/api/users", status_code=status.HTTP_201_CREATED, tags=["User Management"])
def register_graduate(payload: GraduateInput):
    new_id = max([item["id"] for item in graduates_registry], default=100) + 1
    record = {"id": new_id, "full_name": payload.full_name, "contact_email": payload.contact_email}
    graduates_registry.append(record)
    return {"id": new_id, "message": "Successfully registered", "data": record}

@app.put("/api/users/{user_id}", tags=["User Management"])
def overwrite_graduate(user_id: int, payload: GraduateInput):
    match = next((item for item in graduates_registry if item["id"] == user_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Graduate record not found.")
    match["full_name"] = payload.full_name
    match["contact_email"] = payload.contact_email
    return {"message": "Record fully updated", "data": match}

@app.patch("/api/users/{user_id}", tags=["User Management"])
def modify_graduate(user_id: int, payload: GraduatePartialUpdate):
    match = next((item for item in graduates_registry if item["id"] == user_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Graduate record not found.")
    if payload.full_name is not None:
        match["full_name"] = payload.full_name
    if payload.contact_email is not None:
        match["contact_email"] = payload.contact_email
    return {"message": "Record partially modified", "data": match}

@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["User Management"])
def purge_graduate(user_id: int):
    match = next((item for item in graduates_registry if item["id"] == user_id), None)
    if not match:
        raise HTTPException(status_code=404, detail="Graduate record not found.")
    graduates_registry.remove(match)
    return None