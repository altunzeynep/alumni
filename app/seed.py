from app.database import SessionLocal, engine, Base
from app.models import Graduate

def run_seed():
    print("Tablolar oluşturuluyor...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        test_user = Graduate(
            full_name="Ahmet Yılmaz", 
            email="ahmet@example.com", 
            graduation_year=2023
        )
        db.add(test_user)
        db.commit()
        print("Seed verisi başarıyla eklendi!")
    except Exception as e:
        print(f"Hata oluştu: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    run_seed()