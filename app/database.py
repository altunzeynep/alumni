import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Veritabanı URL'si (.env'den veya varsayılan olarak)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:password@postgres:5432/alumni_db")
# Engine tanımı (Eksik olan kısım burası!)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal tanımı
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Veritabanı oturumunu yöneten get_db fonksiyonu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()