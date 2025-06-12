from sqlalchemy.orm import Session
from . import models, schemas

def create_parfum(db: Session, parfum: schemas.ParfumCreate):
    db_parfum = models.Parfum(**parfum.dict())
    db.add(db_parfum)
    db.commit()
    db.refresh(db_parfum)
    return db_parfum

def get_parfums(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Parfum).offset(skip).limit(limit).all()

def get_parfum(db: Session, parfum_id: int):
    return db.query(models.Parfum).filter(models.Parfum.id == parfum_id).first()

def update_parfum(db: Session, parfum_id: int, parfum_update: schemas.ParfumCreate):
    parfum = db.query(models.Parfum).filter(models.Parfum.id == parfum_id).first()
    if not parfum:
        return None
    for field, value in parfum_update.dict().items():
        setattr(parfum, field, value)
    db.commit()
    db.refresh(parfum)
    return parfum

def delete_parfum(db: Session, parfum_id: int):
    parfum = db.query(models.Parfum).filter(models.Parfum.id == parfum_id).first()
    if not parfum:
        return None
    db.delete(parfum)
    db.commit()
    return parfum

def create_kategori(db: Session, kategori: schemas.KategoriCreate):
    db_kategori = models.Kategori(**kategori.dict())
    db.add(db_kategori)
    db.commit()
    db.refresh(db_kategori)
    return db_kategori

def get_kategoris(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Kategori).offset(skip).limit(limit).all()
