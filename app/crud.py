from sqlalchemy.orm import Session
from .import models, schemas
from .utils import hash_password
from app.utils import verify_password
from app.dependencies import ADMIN_EMAILS, ADMIN_PASSWORD
import bcrypt
from sqlalchemy.orm import joinedload


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        return None

    if email == ADMIN_EMAILS and verify_password(password, ADMIN_PASSWORD):
        user.role = "admin"  # ini temporary di sesi login aja
    elif verify_password(password, user.hashed_password):
        user.role = "pembeli"
    else:
        return None

    return user

def get_all_orders(db: Session):
    return db.query(models.Order).options(
        joinedload(models.Order.items).joinedload(models.OrderItem.parfum)
    ).order_by(models.Order.created_at.desc()).all()
    
def get_all_orders_by_zona_waktu(db: Session):
    return db.query(models.Order).options(
        joinedload(models.Order.items).joinedload(models.OrderItem.parfum)
    ).order_by(models.Order.zona_waktu.asc()).all()

# ---------- USER ----------
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = models.User(
        nama=user.nama,
        email=user.email,
        hashed_password=hashed_pw,
        alamat=user.alamat  
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ---------- PARFUM ----------
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

def delete_parfum(db: Session, parfum_id: int):
    parfum = db.query(models.Parfum).filter(models.Parfum.id == parfum_id).first()
    if parfum:
        db.delete(parfum)
        db.commit()
    return parfum

def update_parfum(db: Session, parfum_id: int, parfum_update: schemas.ParfumCreate):
    parfum = db.query(models.Parfum).filter(models.Parfum.id == parfum_id).first()
    if parfum:
        for key, value in parfum_update.dict().items():
            setattr(parfum, key, value)
        db.commit()
        db.refresh(parfum)
    return parfum

def get_parfum_by_name(db: Session, nama: str):
    return db.query(models.Parfum).filter(models.Parfum.nama == nama).first()


# ---------- KATEGORI ----------
def create_kategori(db: Session, kategori: schemas.KategoriCreate):
    db_kategori = models.Kategori(**kategori.dict())
    db.add(db_kategori)
    db.commit()
    db.refresh(db_kategori)
    return db_kategori

def get_kategoris(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Kategori).offset(skip).limit(limit).all()

def get_user_orders(db: Session, user_id: int):
    return (
        db.query(models.Order)
        .filter(models.Order.user_id == user_id)
        .options(joinedload(models.Order.items).joinedload(models.OrderItem.parfum))
        .order_by(models.Order.created_at.desc())
        .all()
    )
