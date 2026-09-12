from sqlalchemy import Column, Integer, BigInteger, String, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from api.database.base import Base
from sqlalchemy.sql import func

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

# Table Guests
class Guest(Base):
    __tablename__ = 'guests'

    id = Column(Integer, primary_key=True, index=True) # Pakai Integer (max 2.1 Miliar)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(25), nullable=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # Relationship ke ClientDevice
    devices = relationship("ClientDevice", back_populates="guest", cascade="all, delete-orphan")


# Table Client Devices
class ClientDevice(Base):
    __tablename__ = "client_devices"

    id = Column(BigInteger, primary_key=True, autoincrement=True) # BigInteger sangat tepat di sini
    
    # PERBAIKAN: Tipe data harus Integer (sama dengan Guest.id) dan tambahkan ForeignKey
    guest_id = Column(Integer, ForeignKey("guests.id", ondelete="CASCADE"), nullable=False, index=True)
    
    mac_add = Column(String(255), nullable=True)
    os_client = Column(String(255), nullable=True)
    browser_client = Column(String(255), nullable=True)
    device_client = Column(String(255), nullable=True)
    brand_client = Column(String(255), nullable=True)
    model_client = Column(String(255), nullable=True)
    device_type = Column(String(255), nullable=True)
    
    # disamakan dengan tabel Guest menggunakan timezone=True
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

    # Relationship ke Guest
    guest = relationship("Guest", back_populates="devices")