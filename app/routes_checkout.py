from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from app import crud
from app.dependencies import get_db, get_current_user
from app.models import Order, OrderItem
from app.schemas import CheckoutItem, CheckoutRequest, CheckoutResponse
from app.utils import detect_timezone_from_address

router = APIRouter()

@router.post("/", response_model=CheckoutResponse)
def checkout(
    data: CheckoutRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    total = 0
    order_items = []

    for item in data.items:
        parfum = crud.get_parfum_by_name(db, item.nama)
        if not parfum:
            raise HTTPException(status_code=404, detail=f"Parfum '{item.nama}' tidak ditemukan")
        total += parfum.harga * item.quantity
        order_items.append({"parfum_id": parfum.id, "quantity": item.quantity})

    alamat_user = current_user.alamat or ""
    zona_waktu = detect_timezone_from_address(alamat_user)

    order = Order(
        user_id=current_user.id,
        total_harga=total,
        zona_waktu=zona_waktu,
        created_at=datetime.utcnow()
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in order_items:
        db_item = OrderItem(order_id=order.id, **item)
        db.add(db_item)

    db.commit()

    return {
        "total_price": total,
        "zona_waktu": zona_waktu,
        "message": "Checkout berhasil"
    }
