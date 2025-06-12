from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user, admin_only
from app.models import Order
from app.schemas import OrderOut
from app import crud
from app.utils import detect_timezone_from_address
from app.models import User  


router = APIRouter()

@router.get("/me", response_model=List[OrderOut])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    orders = (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )

    for order in orders:
        for item in order.items:
            item.parfum  # trigger lazy load

    return orders

@router.get("/admin/orders", response_model=List[OrderOut])
def get_all_orders(
    db: Session = Depends(get_db),
    admin_user = Depends(admin_only)
):
    orders = crud.get_all_orders(db)

    # Update zona waktu dari alamat (jika pakai field alamat_pengiriman)
    for order in orders:
        alamat = order.user.alamat or ""
        order.zona_waktu = detect_timezone_from_address(alamat)

    return orders

@router.put("/admin/update-status/{order_id}")
def update_order_status(order_id: int, status_baru: str, db: Session = Depends(get_db), current_user: User = Depends(admin_only)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order tidak ditemukan")

    order.status_pembayaran = status_baru
    db.commit()
    return {"message": f"Status pesanan {order.id} diubah ke '{status_baru}'"}

@router.get("/status/{order_id}")
def cek_status_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order tidak ditemukan")
    return {"status_pembayaran": order.status_pembayaran}


