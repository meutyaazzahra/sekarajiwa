from app.database import engine, Base
from app.models import Kategori, Parfum, User, Order, OrderItem

print("Membuat tabel di MySQL…")
Base.metadata.create_all(bind=engine)
print("Semua tabel berhasil dibuat!")
