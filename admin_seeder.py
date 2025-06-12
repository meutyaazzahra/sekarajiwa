from app.database import SessionLocal
from app import models, utils

# Ganti ini sesuai data admin kamu
admin_email = "mimin@warisanparfum.com"
admin_password = "miminsyantik"
admin_nama = "Admin Warisan"
admin_alamat = "Purwokerto"

def seed_admin():
    db = SessionLocal()

    existing_admin = db.query(models.User).filter(models.User.email == admin_email).first()
    if existing_admin:
        print("Admin sudah ada di database.")
        return

    hashed_pw = utils.hash_password(admin_password)
    admin_user = models.User(
        nama=admin_nama,
        email=admin_email,
        hashed_password=hashed_pw,
        alamat=admin_alamat,
        is_active=True
    )

    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    print("Admin berhasil dibuat dengan ID:", admin_user.id)

if __name__ == "__main__":
    seed_admin()
