import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def detect_timezone_from_address(alamat: str) -> str:
    if not alamat or not isinstance(alamat, str):
        return "WIB"
    alamat_lower = alamat.lower()
    if any(region.lower() in alamat_lower for region in ["Aceh", "Sumatera Utara", "Sumatera Barat", "Riau", "Kepulauan Riau", "Jambi", "Bengkulu", "Sumatera Selatan", "Kep. Bangka Belitung", "Lampung", "DKI Jakarta", "Banten", "Jawa Barat", "Jawa Tengah", "DI Yogyakarta", "Jawa Timur"]):
        return "WIB"
    elif any(region.lower() in alamat_lower for region in ["Bali", "Nusa Tenggara Barat", "Nusa Tenggara Timur", "Kalimantan Tengah", "Kalimantan Selatan", "Kalimantan Timur", "Kalimantan Utara", "Sulawesi Utara", "Gorontalo", "Sulawesi Tengah", "Sulawesi Barat", "Sulawesi Selatan", "Sulawesi Tenggara"]):
        return "WITA"
    elif any(region.lower() in alamat_lower for region in ["Maluku", "Maluku Utara", "Papua", "Papua Barat", "Papua Selatan", "Papua Tengah", "Papua Pegunungan", "Papua Barat Daya"]):
        return "WIT"
    else:
        return "WIB"
