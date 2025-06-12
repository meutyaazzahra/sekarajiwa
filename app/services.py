from sqlalchemy.orm import Session
from . import schemas, repositories

def create_parfum(db: Session, parfum: schemas.ParfumCreate):
    return repositories.create_parfum(db, parfum)

def get_parfums(db: Session, skip: int = 0, limit: int = 100):
    return repositories.get_parfums(db, skip, limit)

def get_parfum(db: Session, parfum_id: int):
    return repositories.get_parfum(db, parfum_id)

def update_parfum(db: Session, parfum_id: int, parfum_data: schemas.ParfumCreate):
    return repositories.update_parfum(db, parfum_id, parfum_data)

def delete_parfum(db: Session, parfum_id: int):
    return repositories.delete_parfum(db, parfum_id)

def create_kategori(db: Session, kategori: schemas.KategoriCreate):
    return repositories.create_kategori(db, kategori)

def get_kategoris(db: Session, skip: int = 0, limit: int = 100):
    return repositories.get_kategoris(db, skip, limit)
