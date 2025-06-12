# reset_db.py
from app.database import SessionLocal
from app import models

def clear_kategoris():
    db = SessionLocal()
    db.query(models.Kategori).delete()
    db.commit()
    db.close()
    print("Tabel kategoris berhasil dikosongkan.")

if __name__ == "__main__":
    clear_kategoris()
