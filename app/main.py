from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from . import models, schemas, crud, database
from .dependencies import get_db
from .utils import verify_password
from .auth import create_access_token

from .checkout import router as checkout_router
from .routers import routers_order
import logging

logging.basicConfig(level=logging.DEBUG)

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # GANTI dengan IP frontend Laravel kalau mau lebih aman
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Auth
@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")
    return crud.create_user(db=db, user=user)

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email atau password salah")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# Routers
app.include_router(checkout_router, prefix="/checkout", tags=["Checkout"])
app.include_router(routers_order.router, prefix="/orders", tags=["Orders"]) 

# Parfum
@app.post("/parfums/", response_model=schemas.Parfum)
def create_parfum(parfum: schemas.ParfumCreate, db: Session = Depends(get_db)):
    return crud.create_parfum(db, parfum)

@app.get("/parfums/", response_model=list[schemas.Parfum])
def read_parfums(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_parfums(db, skip, limit)

@app.get("/parfums/{parfum_id}", response_model=schemas.Parfum)
def read_parfum(parfum_id: int, db: Session = Depends(get_db)):
    parfum = crud.get_parfum(db, parfum_id)
    if not parfum:
        raise HTTPException(status_code=404, detail="Parfum not found")
    return parfum

@app.delete("/parfums/{parfum_id}", response_model=schemas.Parfum)
def delete_parfum(parfum_id: int, db: Session = Depends(get_db)):
    parfum = crud.delete_parfum(db, parfum_id)
    if not parfum:
        raise HTTPException(status_code=404, detail="Parfum not found")
    return parfum

@app.put("/parfums/{parfum_id}", response_model=schemas.Parfum)
def update_parfum(parfum_id: int, parfum_data: schemas.ParfumCreate, db: Session = Depends(get_db)):
    parfum = crud.update_parfum(db, parfum_id, parfum_data)
    if not parfum:
        raise HTTPException(status_code=404, detail="Parfum not found")
    return parfum

# Kategori
@app.post("/kategoris/", response_model=schemas.Kategori)
def create_kategori(kategori: schemas.KategoriCreate, db: Session = Depends(get_db)):
    return crud.create_kategori(db, kategori)

@app.get("/kategoris/", response_model=list[schemas.Kategori])
def read_kategoris(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_kategoris(db, skip, limit)

from .routers import routes_payment
app.include_router(routes_payment.router)

