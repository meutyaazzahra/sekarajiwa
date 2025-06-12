from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db, admin_only

router = APIRouter()

@router.post("/kategoris")
def create_kategori(
    kategori: schemas.KategoriCreate,
    db: Session = Depends(get_db),
    current_user = Depends(admin_only)
):
    return crud.create_kategori(db, kategori)
