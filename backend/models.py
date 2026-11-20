from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    agent_age: Mapped[int] = mapped_column(Integer)
    agent_rating: Mapped[float] = mapped_column(Float)
    weather: Mapped[str] = mapped_column(String(20))
    traffic: Mapped[str] = mapped_column(String(20))
    vehicle: Mapped[str] = mapped_column(String(20))
    area: Mapped[str] = mapped_column(String(20))
    category: Mapped[str] = mapped_column(String(30))
    distance_km: Mapped[float] = mapped_column(Float)
    departure_time: Mapped[datetime] = mapped_column(DateTime)
    predicted_minutes: Mapped[float] = mapped_column(Float)
    model_version: Mapped[str] = mapped_column(String(20))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="user")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())