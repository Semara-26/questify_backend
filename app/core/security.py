import os
import re
from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

# Konfigurasi Hashing Password dengan algoritma Bcrypt (Minimal 12 rounds)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

# Mengambil konfigurasi JWT dari Environment Variables
# Variabel environment harus di-load (misal dari file .env) di luar aplikasi
SECRET_KEY = os.getenv("SECRET_KEY", "FALLBACK_SECRET_KEY_YANG_SANGAT_RAHASIA")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def validate_password_strength(password: str) -> None:
    """
    Validasi kekuatan password.
    Syarat: Minimal 8 karakter dan mengandung setidaknya 1 angka.
    """
    if len(password) < 8:
        raise ValueError("Password harus memiliki minimal 8 karakter.")
    if not re.search(r"\d", password):
        raise ValueError("Password harus mengandung setidaknya satu angka.")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifikasi kecocokan antara password plain text dan hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Memvalidasi dan menghasilkan hash bcrypt dari password plain text.
    Melemparkan ValueError jika password tidak memenuhi standar keamanan.
    """
    validate_password_strength(password)
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    """
    Membuat JWT token berdasarkan payload data yang diberikan.
    Expire time diambil dari Environment Variables.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
