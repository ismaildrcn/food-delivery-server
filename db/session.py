from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from db.models.base import Base
from db.models.user import User
from dotenv import load_dotenv
import os

# Çevresel değişkenleri yükle
load_dotenv()

# PostgreSQL bağlantı URL'si
DATABASE_URL = os.getenv("DATABASE_URL")

# Veritabanı motoru oluştur
engine = create_engine(DATABASE_URL)

# Veritabanı yoksa oluştur
if not database_exists(engine.url):
    create_database(engine.url)
    print("Veritabanı oluşturuldu!")
else:
    print("Veritabanı zaten var.")

# Oturum fabrikası oluştur
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Veritabanı tablolarını oluştur (eğer yoksa)
Base.metadata.create_all(bind=engine)

# Dependency olarak kullanılacak oturum fonksiyonu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()