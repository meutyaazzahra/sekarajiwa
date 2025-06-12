from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.dependencies import get_db, admin_only

router = APIRouter()

@router.post("/parfums")
def create_parfum(
    parfum: schemas.ParfumCreate,
    db: Session = Depends(get_db),
    current_user = Depends(admin_only)
):
    return crud.create_parfum(db, parfum)

@router.put("/parfums/{parfum_id}")
def update_parfum(
    parfum_id: int,
    parfum_update: schemas.ParfumCreate,
    db: Session = Depends(get_db),
    current_user = Depends(admin_only)
):
    updated = crud.update_parfum(db, parfum_id, parfum_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Parfum tidak ditemukan")
    return updated

@router.delete("/parfums/{parfum_id}")
def delete_parfum(
    parfum_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(admin_only)
):
    deleted = crud.delete_parfum(db, parfum_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Parfum tidak ditemukan")
    return {"message": "Parfum berhasil dihapus"}
