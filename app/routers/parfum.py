# app/routers/parfum.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/parfums", response_model=list[schemas.Parfum])
def read_parfums(db: Session = Depends(get_db)):
    return crud.get_parfums(db)

@router.post("/parfums", response_model=schemas.Parfum)
def create_parfum(parfum: schemas.ParfumCreate, db: Session = Depends(get_db)):
    return crud.create_parfum(db, parfum)
