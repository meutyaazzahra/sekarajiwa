from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Parfum, Order, OrderItem
from datetime import datetime

db: Session = SessionLocal()

# Ambil user yang sudah ada
user = db.query(User).first()
if not user:
    print("User belum ada di database.")
    exit()

# Ambil parfum yang tersedia
parfum = db.query(Parfum).first()
if not parfum:
    print("Parfum belum ada di database.")
    exit()

# Buat order baru
order = Order(user_id=user.id, total_harga=parfum.harga * 2, created_at=datetime.utcnow())
db.add(order)
db.commit()
db.refresh(order)

# Buat item pesanan
order_item = OrderItem(order_id=order.id, parfum_id=parfum.id, quantity=2)
db.add(order_item)
db.commit()

print(f"Berhasil buat order id={order.id} untuk user={user.email}")
