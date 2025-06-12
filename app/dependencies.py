from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import crud
from .auth import verify_token
from .database import SessionLocal

# OAuth2 skema token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Daftar email admin yang diizinkan
ADMIN_EMAILS = ["mimin@warisanparfum.com"]
ADMIN_PASSWORD = "miminsyantik"

# Ambil koneksi DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ambil user yang sedang login dari token
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user_id = verify_token(token)  # return user_id (string) dari payload["sub"]
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau sudah kadaluarsa",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = crud.get_user_by_id(db, int(user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User tidak ditemukan",
        )
    return user

# Khusus akses admin
def admin_only(current_user = Depends(get_current_user)):
    if current_user.email not in ADMIN_EMAILS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Akses khusus admin",
        )
    return current_user
