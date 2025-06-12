from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Kategori(Base):
    __tablename__ = "kategoris"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(255), unique=True, index=True)

    parfums = relationship("Parfum", back_populates="kategori")


class Parfum(Base):
    __tablename__ = "parfums"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(255), index=True)
    deskripsi = Column(String(255))
    harga = Column(Float)
    stok = Column(Integer, default=0)
    gambar = Column(String(255), nullable=True)
    kategori_id = Column(Integer, ForeignKey("kategoris.id"), nullable=False)

    kategori = relationship("Kategori", back_populates="parfums")
    order_items = relationship("OrderItem", back_populates="parfum")  


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    alamat = Column(String(255), nullable=True)  
    is_active = Column(Boolean, default=True)

    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_harga = Column(Float)
    zona_waktu = Column(String(20))  # baru
    alamat_pengiriman = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    status_pembayaran = Column(String, default="Menunggu Pembayaran")  

    
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    parfum_id = Column(Integer, ForeignKey("parfums.id"))
    quantity = Column(Integer)

    order = relationship("Order", back_populates="items")
    parfum = relationship("Parfum", back_populates="order_items")