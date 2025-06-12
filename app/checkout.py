from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from app import crud
from app.dependencies import get_db, get_current_user
from app.models import Order, OrderItem

router = APIRouter()

# Skema input
class CheckoutItem(BaseModel):
    nama: str
    quantity: int

class CheckoutRequest(BaseModel):
    items: List[CheckoutItem]

# Skema output
class CheckoutResponse(BaseModel):
    total_price: float
    message: str

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
        subtotal = parfum.harga * item.quantity
        total += subtotal

        order_item = OrderItem(
            parfum_id=parfum.id,
            quantity=item.quantity,
        )
        order_items.append(order_item)

    new_order = Order(
        user_id=current_user.id,
        total_harga=total,
        items=order_items
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {
        "total_price": total,
        "message": f"Checkout berhasil! Order ID: {new_order.id}"
    }
