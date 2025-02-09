from sqlalchemy import Column, Integer, String
from db.models.base import Base  # Base sınıfını içe aktarıyoruz

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, index=True, nullable=True)
    last_name = Column(String, index=True, nullable=True)
    country_code = Column(Integer, index=True, nullable=True)
    phone_number = Column(String, index=True, nullable=True)
    password = Column(String, nullable=False)