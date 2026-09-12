from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP, text
from sqlalchemy.sql import func
from api.database.base import Base

#Table Users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(300), nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    email_verified_at = Column(TIMESTAMP(timezone=True), nullable=True)
    password = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    role = Column(String(50), nullable=False, default="user")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

#Table Guests
class Guest(Base):
    __tablename__ = 'guests'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(25), nullable=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

