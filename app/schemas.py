from pydantic import BaseModel, EmailStr, field_serializer
from typing import List
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    nama: str
    alamat: str  

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ParfumBase(BaseModel):
    nama: str
    deskripsi: str
    stok: int

class ParfumCreate(ParfumBase):
    pass

class Parfum(ParfumBase):
    id: int

    class Config:
        orm_mode = True

class KategoriBase(BaseModel):
    nama: str

class KategoriCreate(KategoriBase):
    pass

class Kategori(KategoriBase):
    id: int

    class Config:
        orm_mode = True

class CheckoutItem(BaseModel):
    nama: str
    quantity: int

class CheckoutRequest(BaseModel):
    items: List[CheckoutItem]

class CheckoutResponse(BaseModel):
    total_price: float
    zona_waktu: str
    message: str

class ParfumOut(BaseModel):
    nama: str

    class Config:
        orm_mode = True

class OrderItemOut(BaseModel):
    parfum: ParfumOut
    quantity: int

    class Config:
        orm_mode = True

class OrderOut(BaseModel):
    id: int
    total_harga: float
    zona_waktu: Optional[str] = None        
    status_pembayaran: str
    created_at: datetime
    items: List[OrderItemOut]

    @field_serializer("created_at")
    def serialize_created_at(self, created_at: datetime, _info):
        return created_at.strftime("%d-%m-%Y %H:%M:%S")

    class Config:
        from_attributes = True
