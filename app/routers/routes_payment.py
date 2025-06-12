from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..models import Order, User
from ..database import get_db
from ..dependencies import get_current_user


router = APIRouter()

@router.post("/bayar/{order_id}")
def bayar_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order tidak ditemukan")

    if order.status_pembayaran != "Menunggu Pembayaran":
        raise HTTPException(status_code=400, detail="Order sudah dibayar atau sedang diproses")

    # Simulasikan pembayaran berhasil
    order.status_pembayaran = "Sudah Dibayar"
    db.commit()

    return {"message": "Pembayaran berhasil", "order_id": order.id}
