from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
from app.dependencies import get_current_admin_user

router = APIRouter(
    prefix="/admin/parfums",
    tags=["Admin - Kelola Parfum"]
)

# GET semua parfum
@router.get("/", response_model=list[schemas.Parfum])
def read_parfums(db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin_user)):
    return crud.get_parfums(db)

# GET satu parfum by ID
@router.get("/{parfum_id}", response_model=schemas.Parfum)
def read_parfum(parfum_id: int, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin_user)):
    parfum = crud.get_parfum(db, parfum_id)
    if not parfum:
        raise HTTPException(status_code=404, detail="Parfum tidak ditemukan")
    return parfum

# POST tambah parfum baru
@router.post("/", response_model=schemas.Parfum)
def create_parfum(parfum: schemas.ParfumCreate, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin_user)):
    return crud.create_parfum(db, parfum)

# PUT update parfum
@router.put("/{parfum_id}", response_model=schemas.Parfum)
def update_parfum(parfum_id: int, parfum_update: schemas.ParfumCreate, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin_user)):
    parfum = crud.update_parfum(db, parfum_id, parfum_update)
    if not parfum:
        raise HTTPException(status_code=404, detail="Parfum tidak ditemukan")
    return parfum

# DELETE hapus parfum
@router.delete("/{parfum_id}")
def delete_parfum(parfum_id: int, db: Session = Depends(get_db), current_admin: models.User = Depends(get_current_admin_user)):
    parfum = crud.delete_parfum(db, parfum_id)
    if not parfum:
        raise HTTPException(status_code=404, detail="Parfum tidak ditemukan")
    return {"message": "Parfum berhasil dihapus"}
