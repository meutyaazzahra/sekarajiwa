from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Kategori, Parfum

kategori_data = [{"nama": "Parfum Warisan"}]

parfum_data = [
    {"nama": "Kenanga Senja", "deskripsi": "Aroma floral manis dengan sentuhan vanila & kayu.", "harga": 210000, "gambar": None},
    {"nama": "Sukma Laut",    "deskripsi": "Segar laut & rempah lembut, inspirasi dari lautan timur.",        "harga": 230000, "gambar": None}, 
    {"nama": "Larasati",      "deskripsi": "Elegan, spicy floral, cocok untuk malam hari.",                    "harga": 260000, "gambar": None},
    {"nama": "Kinasih",       "deskripsi": "Romantis, melati, mawar, dan amber.",                             "harga": 240000, "gambar": None},
    {"nama": "Banyu Langit",  "deskripsi": "Citrusy segar dengan hint pandan & green tea.",                   "harga": 220000, "gambar": None},
    {"nama": "Cempaka Wangi", "deskripsi": "Aroma floral cempaka khas Jawa yang lembut dengan sentuhan musk dan kayu manis.", "harga": 210000, "gambar": None},
    {"nama": "Melati Pagi", "deskripsi": "Segar dan manis melati dipadu dengan aroma jeruk nipis dan sedikit vanila.", "harga": 200000, "gambar": None},
    {"nama": "Srikaya Malam", "deskripsi": "Perpaduan aroma buah srikaya yang manis dan sedikit spicy dengan nuansa kayu gaharu.", "harga": 230000, "gambar": None},
    {"nama": "Gending Asmara", "deskripsi": "Kombinasi mawar merah dan ylang-ylang yang menggoda, cocok untuk suasana romantis.", "harga": 225000, "gambar": None},
    {"nama": "Tirta Arum", "deskripsi": "Wangi segar air dan bunga lotus dengan sentuhan green tea dan bambu.", "harga": 215000, "gambar": None},
    {"nama": "Angin Surya", "deskripsi": "Aroma citrus jeruk bali yang segar dengan hint jahe dan daun serai.", "harga": 205000, "gambar": None},
    {"nama": "Kembang Sepatu", "deskripsi": "Manis floral dari bunga sepatu dengan aksen vanilla dan sandalwood.", "harga": 210000, "gambar": None},
    {"nama": "Rembulan Sari", "deskripsi": "Aroma malam dengan campuran melati, cendana, dan sedikit musk yang memikat.", "harga": 230000, "gambar": None},
    {"nama": "Puspa Luhur", "deskripsi": "Wangi rempah khas nusantara, kayu manis, kapulaga, dan bunga kenanga.", "harga": 220000, "gambar": None},
    {"nama": "Bayu Lautan", "deskripsi": "Aroma segar laut, campuran lemon, daun pandan, dan sedikit aroma garam laut.", "harga": 215000, "gambar": None}
]

def seed():
    db: Session = SessionLocal()
    try:
        # Insert kategori jika belum ada
        for k in kategori_data:
            if not db.query(Kategori).filter_by(nama=k["nama"]).first():
                db.add(Kategori(nama=k["nama"]))
        db.commit()

        # Ambil kategori Warisan
        kategori = db.query(Kategori).filter_by(nama="Parfum Warisan").first()

        # Insert setiap parfum jika belum ada
        for p in parfum_data:
            if not db.query(Parfum).filter_by(nama=p["nama"]).first():
                db.add(Parfum(
                    nama=p["nama"],
                    deskripsi=p["deskripsi"],
                    harga=p["harga"],
                    gambar=p["gambar"],
                    kategori_id=kategori.id
                ))
        db.commit()
        print("Semua data parfum berhasil dimasukkan!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
