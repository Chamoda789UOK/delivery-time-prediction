from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PredictionRequest(BaseModel):
    agent_age: int = Field(ge=15, le=50)
    agent_rating: float = Field(ge=1, le=5)
    weather: Literal["Sunny", "Cloudy", "Fog", "Stormy", "Sandstorms", "Windy"]
    traffic: Literal["Low", "Medium", "High", "Jam"]
    vehicle: Literal["motorcycle", "scooter", "van"]
    area: Literal["Metropolitan", "Urban", "Semi-Urban", "Other"]
    category: Literal[
        "Electronics", "Books", "Jewelry", "Toys", "Skincare", "Snacks",
        "Outdoors", "Apparel", "Sports", "Grocery", "Pet Supplies", "Home",
        "Cosmetics", "Kitchen", "Clothing", "Shoes",
    ]
    distance_km: float = Field(gt=0, le=25)
    departure_time: datetime


class PredictionResponse(BaseModel):
    id: int
    predicted_minutes: float
    estimated_arrival: datetime
    model_version: str
    note: str


class PredictionRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    agent_age: int
    agent_rating: float
    weather: str
    traffic: str
    vehicle: str
    area: str
    category: str
    distance_km: float
    departure_time: datetime
    predicted_minutes: float
    model_version: str
    created_at: datetime