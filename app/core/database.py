import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Muat environment variables dari .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("FATAL: DATABASE_URL environment variable is not set!")

# Konfigurasi parameter engine agar ramah memori (RAM < 512MB)
engine = create_engine(
    DATABASE_URL,
    pool_size=5,  # Membatasi koneksi permanen maksimum (hemat memori)
    max_overflow=10,  # Batas koneksi tambahan saat traffic tinggi
    pool_timeout=30,  # Waktu tunggu maksimal untuk mendapat koneksi (detik)
    pool_recycle=1800,  # Daur ulang koneksi setiap 30 menit
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
